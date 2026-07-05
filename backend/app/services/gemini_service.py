import json
import re
from typing import Dict, Any, Optional
import google.generativeai as genai
from backend.app.config.config import settings

# Initialize Gemini Client
if settings.gemini_api_key and settings.gemini_api_key != "dummy_key":
    genai.configure(api_key=settings.gemini_api_key)

SCHEMA_CONTEXT = """
You are a MySQL database expert specializing in cricket analytics. Translate the user's natural language question into a single valid MySQL SELECT query.

### Database Schema:
1. Table `teams`:
   - `team_id`: INT (Primary Key)
   - `team_name`: VARCHAR (e.g. 'Royal Challengers Bangalore', 'Kolkata Knight Riders')
   - `team_name_short`: VARCHAR (e.g. 'RCB', 'KKR')
   - `image_url`: TEXT

2. Table `player_info`:
   - `player_id`: INT (Primary Key)
   - `player_name`: VARCHAR (e.g. 'V Kohli', 'MS Dhoni' - short names used in matches)
   - `bat_style`: VARCHAR ('Right hand Bat', 'Left hand Bat')
   - `bowl_style`: VARCHAR ('Right arm Medium', 'Legbreak Googly', etc.)
   - `field_pos`: VARCHAR ('Wicketkeeper', etc.)
   - `player_full_name`: VARCHAR (e.g. 'Virat Kohli')
   - `player_name2`: VARCHAR
   - `player_image`: TEXT

3. Table `ipl_match`:
   - `match_id`: INT (Primary Key)
   - `season_id`: INT
   - `balls_per_over`: INT (usually 6)
   - `city`: VARCHAR (e.g. 'Bangalore', 'Mumbai')
   - `match_date`: VARCHAR (format 'DD-MM-YYYY')
   - `event_name`: VARCHAR ('Indian Premier League')
   - `match_number`: INT
   - `gender`: VARCHAR ('male')
   - `match_type`: VARCHAR ('league match', etc.)
   - `format`: VARCHAR ('T20')
   - `overs`: INT (usually 20)
   - `season`: VARCHAR (e.g. '2008', '2024')
   - `team_type`: VARCHAR ('club')
   - `venue`: VARCHAR (e.g. 'M Chinnaswamy Stadium')
   - `toss_winner`: VARCHAR (team name)
   - `team1`: VARCHAR (team name)
   - `team2`: VARCHAR (team name)
   - `toss_decision`: VARCHAR ('field' or 'bat')
   - `match_winner`: VARCHAR (team name)
   - `win_by_runs`: INT
   - `win_by_wickets`: INT
   - `player_of_match`: INT (foreign key referring to player_info.player_id)
   - `result`: VARCHAR ('win', 'tie', etc.)
   - `stage`: VARCHAR

4. Table `ball_by_ball`:
   - `season_id`: INT
   - `match_id`: INT (foreign key referring to ipl_match.match_id)
   - `batter`: VARCHAR (short name string matching player_info.player_name, e.g. 'V Kohli')
   - `bowler`: VARCHAR (short name string matching player_info.player_name, e.g. 'I Sharma')
   - `non_striker`: VARCHAR (player name string)
   - `team_batting`: VARCHAR (team name string)
   - `team_bowling`: VARCHAR (team name string)
   - `over_number`: INT (0 to 19 for a normal T20 match)
   - `ball_number`: INT (0-indexed delivery in the over)
   - `batter_runs`: INT (runs scored by the batter off the bat)
   - `extras`: INT (runs from extras: wide, no ball, bye, leg-bye)
   - `total_runs`: INT (batter_runs + extras)
   - `batsman_type`: VARCHAR ('Right hand Bat', 'Left hand Bat')
   - `bowler_type`: VARCHAR ('Right arm Medium', 'Slow Left arm Orthodox', etc.)
   - `player_out`: VARCHAR (name of player out, or 'NULL' / None if no wicket)
   - `fielders_involved`: VARCHAR
   - `is_wicket`: BOOLEAN (True/1 if a wicket fell, False/0 otherwise)
   - `is_wide_ball`: BOOLEAN
   - `is_no_ball`: BOOLEAN
   - `is_leg_bye`: BOOLEAN
   - `is_bye`: BOOLEAN
   - `is_penalty`: BOOLEAN
   - `wide_ball_runs`: INT
   - `no_ball_runs`: INT
   - `leg_bye_runs`: INT
   - `bye_runs`: INT
   - `penalty_runs`: INT
   - `wicket_kind`: VARCHAR ('caught', 'bowled', 'run out', 'lbw', 'stumped', etc.)
   - `is_super_over`: BOOLEAN
   - `innings`: INT (1 or 2)

### Cricket Analytics Calculations:
- **Runs Scored**: Use `SUM(batter_runs)` from `ball_by_ball`.
- **Balls Faced**: Count deliveries in `ball_by_ball` where `is_wide_ball = 0` (wide balls do not count as a ball faced for a batter).
- **Batting Strike Rate**: `(SUM(batter_runs) / COUNT(CASE WHEN is_wide_ball = 0 THEN 1 END)) * 100`
- **Batting Average**: `SUM(batter_runs) / NULLIF(COUNT(CASE WHEN is_wicket = 1 AND player_out IS NOT NULL AND player_out != 'NULL' THEN 1 END), 0)` (or division by total matches / dismissals).
- **Bowling Wickets**: Count of deliveries where `is_wicket = 1` and `wicket_kind` NOT IN ('run out', 'retired hurt', 'obstructing the field').
- **Runs Conceded by Bowler**: `SUM(batter_runs + wide_ball_runs + no_ball_runs)` (byes and leg-byes are NOT credited as runs conceded by the bowler).
- **Overs Bowled**: `COUNT(CASE WHEN is_wide_ball = 0 AND is_no_ball = 0 THEN 1 END) / 6.0` (each over contains 6 legal balls).
- **Economy Rate**: `(SUM(batter_runs + wide_ball_runs + no_ball_runs) / (COUNT(CASE WHEN is_wide_ball = 0 AND is_no_ball = 0 THEN 1 END) / 6.0))`

### Constraints:
1. Always output ONLY valid MySQL SELECT query. Do not include markdown code block syntax (like ```sql) in the JSON payload fields.
2. Join `player_info` by short names: `player_info.player_name = ball_by_ball.batter` or `player_info.player_name = ball_by_ball.bowler`.
3. To find a player, perform case-insensitive checks on both `player_name` (e.g. 'V Kohli') and `player_full_name` (e.g. 'Virat Kohli').

### Response Format:
You MUST return a JSON object with the following structure:
{
  "sql": "SELECT ...",
  "recommended_chart": {
    "type": "bar" | "line" | "pie" | "radar" | "area" | "table",
    "x_axis": "column_name_for_x_axis",
    "y_axis": "column_name_for_y_axis",
    "title": "Chart Title"
  }
}
"""

class GeminiService:
    @staticmethod
    def generate_sql(user_query: str) -> Dict[str, Any]:
        """
        Translates a natural language query into SQL and recommends a chart.
        """
        if not settings.gemini_api_key or settings.gemini_api_key == "dummy_key":
            return {
                "sql": "SELECT 'Please configure GEMINI_API_KEY in .env file to generate dynamic SQL queries.' AS message;",
                "recommended_chart": {"type": "table", "x_axis": "message", "y_axis": "", "title": "API Configuration Required"}
            }

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"{SCHEMA_CONTEXT}\n\nUser Question: {user_query}\n\nResponse (JSON format only):"
            
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            result = json.loads(response.text)
            return result
        except Exception as e:
            # Fallback in case of errors
            print(f"Error in Gemini SQL Generation: {e}")
            return {
                "sql": f"SELECT 'Error generating SQL: {str(e)}' AS error;",
                "recommended_chart": {"type": "table", "x_axis": "error", "y_axis": "", "title": "Generation Failed"}
            }

    @staticmethod
    def generate_explanation(user_query: str, sql_query: str, results: list) -> str:
        """
        Generates a natural language explanation of the database query results.
        """
        if not settings.gemini_api_key or settings.gemini_api_key == "dummy_key":
            return "Local execution: Please configure your Gemini API Key to see full natural language analysis."

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Format results snippet for the prompt context
            results_snippet = json.dumps(results[:10], indent=2)
            if len(results) > 10:
                results_snippet += f"\n... (and {len(results) - 10} more rows)"

            prompt = (
                "You are an insightful IPL cricket commentator and data analyst. Explain the results of a database query in a professional, engaging way.\n\n"
                f"User Question: {user_query}\n"
                f"SQL Query Executed: {sql_query}\n"
                f"Results:\n{results_snippet}\n\n"
                "Write a clear, concise summary (2-3 sentences) explaining the key insights from these results."
            )
            
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return "Successfully retrieved data. Configure the Gemini API key for advanced analysis."

    @staticmethod
    def repair_sql(failed_sql: str, error_message: str, user_query: str) -> Dict[str, Any]:
        """
        Attempts to repair a failed SQL statement based on the SQL error message.
        """
        if not settings.gemini_api_key or settings.gemini_api_key == "dummy_key":
            return {"sql": failed_sql}

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = (
                f"{SCHEMA_CONTEXT}\n\n"
                "A previously generated SQL query failed to execute. Fix the query to run correctly on MySQL.\n\n"
                f"Original User Question: {user_query}\n"
                f"Failed SQL: {failed_sql}\n"
                f"MySQL Error Message: {error_message}\n\n"
                "Return a corrected JSON object matching the standard response format containing the corrected SQL."
            )
            
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            result = json.loads(response.text)
            return result
        except Exception as e:
            print(f"SQL repair service failed: {e}")
            return {"sql": failed_sql}
