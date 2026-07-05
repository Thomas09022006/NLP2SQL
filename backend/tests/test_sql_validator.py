import unittest
import sys
import os

# Add the project root to sys.path to enable backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.validators.sql_validator import validate_sql_query

class TestSqlValidator(unittest.TestCase):
    def test_valid_select_queries(self):
        # Test standard SELECT queries
        queries = [
            "SELECT * FROM teams",
            "SELECT team_id, team_name FROM teams WHERE team_name_short = 'RCB'",
            "SELECT COUNT(*), season FROM ipl_match GROUP BY season",
            "SELECT m.season, b.batter, SUM(b.batter_runs) FROM ball_by_ball b JOIN ipl_match m ON b.match_id = m.match_id GROUP BY m.season, b.batter",
            "   SELECT * FROM player_info   ",  # Leading/trailing whitespace
            "SeLeCt * FrOm teams",            # Mixed case keywords
        ]
        for query in queries:
            is_valid, err = validate_sql_query(query)
            self.assertTrue(is_valid, f"Query failed validation: {query}. Error: {err}")
            self.assertEqual(err, "")

    def test_valid_with_cte_queries(self):
        # Test valid CTEs (WITH queries)
        queries = [
            "WITH season_runs AS (SELECT match_id, SUM(batter_runs) as runs FROM ball_by_ball GROUP BY match_id) SELECT * FROM season_runs",
            "WITH cte1 AS (SELECT player_id FROM player_info), cte2 AS (SELECT match_id FROM ipl_match) SELECT * FROM cte1 CROSS JOIN cte2",
        ]
        for query in queries:
            is_valid, err = validate_sql_query(query)
            self.assertTrue(is_valid, f"CTE query failed validation: {query}. Error: {err}")
            self.assertEqual(err, "")

    def test_invalid_multi_statements(self):
        # Test forbidden multiple SQL statements separated by semicolon
        queries = [
            "SELECT * FROM teams; SELECT * FROM player_info",
            "SELECT * FROM teams; DROP TABLE player_info",
            "SELECT * FROM teams; ;",
        ]
        for query in queries:
            is_valid, err = validate_sql_query(query)
            self.assertFalse(is_valid, f"Multi-statement query incorrectly passed: {query}")
            self.assertIn("multiple SQL statements is forbidden", err)

    def test_invalid_non_select_start(self):
        # Test query not starting with SELECT or WITH
        queries = [
            "INSERT INTO teams (team_name) VALUES ('Test')",
            "UPDATE player_info SET player_name = 'Modified'",
            "DELETE FROM teams WHERE team_id = 1",
            "DROP TABLE teams",
            "SHOW DATABASES",
        ]
        for query in queries:
            is_valid, err = validate_sql_query(query)
            self.assertFalse(is_valid, f"Non-SELECT query starting word passed: {query}")
            self.assertIn("Only SELECT or WITH statements are allowed", err)

    def test_invalid_forbidden_keywords_within_select(self):
        # Test SELECT statements containing destructive/forbidden keyword operations
        forbidden = [
            "SELECT * FROM teams WHERE team_name = (DELETE FROM teams)",
            "SELECT * FROM player_info UNION SELECT drop_table()",
            "SELECT * FROM teams INTO OUTFILE '/tmp/teams.csv'",
            "SELECT * FROM teams INTO DUMPFILE '/tmp/teams.bin'",
            "SELECT ALTER TABLE teams ADD COLUMN x INT",
            "SELECT TRUNCATE TABLE teams",
            "SELECT CREATE TABLE test (id INT)",
        ]
        for query in forbidden:
            is_valid, err = validate_sql_query(query)
            self.assertFalse(is_valid, f"Query containing forbidden keyword passed: {query}")
            self.assertIn("Dangerous SQL operation detected", err)

if __name__ == "__main__":
    unittest.main()
