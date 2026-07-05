import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Database, 
  Terminal, 
  Play, 
  Settings, 
  History, 
  User, 
  Sun, 
  Moon, 
  ChevronRight,
  TrendingUp,
  Cpu,
  Shield,
  Layers,
  Search,
  LogOut,
  Clock,
  Bookmark,
  AlertTriangle,
  CheckCircle,
  Copy,
  Download,
  PlusCircle,
  ArrowRight,
  Code,
  FileSpreadsheet,
  X,
  Trash2
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

// Color Palette for Recharts
const CHART_COLORS = ['#5673ff', '#818cf8', '#34d399', '#f43f5e', '#fbbf24', '#a78bfa', '#22d3ee'];

// Helper to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('cricsql_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// ==========================================
// Main Layout Component
// ==========================================
const Layout = ({ children, darkMode, setDarkMode, user, onLogout }) => {
  return (
    <div className="min-h-screen bg-slate-50 text-gray-900 dark:bg-dark dark:text-gray-100 transition-colors duration-200">
      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-dark-paper/70 backdrop-blur-md sticky top-0 z-50 px-4 md:px-6 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-2">
          <div className="bg-brand-500 p-2 rounded-xl text-white shadow-lg shadow-brand-500/30">
            <Database size={20} className="animate-pulse-slow" />
          </div>
          <span className="font-extrabold text-lg md:text-xl tracking-tight bg-gradient-to-r from-brand-500 to-indigo-400 bg-clip-text text-transparent">
            CricSQL
          </span>
          <span className="hidden sm:inline-block text-[10px] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-medium">
            AI Analytics
          </span>
        </Link>

        <div className="flex items-center gap-3 md:gap-4">
          <button 
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-lg bg-gray-100 dark:bg-dark-muted hover:bg-gray-200 dark:hover:bg-gray-700 transition"
            aria-label="Toggle Dark Mode"
          >
            {darkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>
          
          {user ? (
            <div className="flex items-center gap-2 md:gap-4">
              <span className="hidden md:inline text-sm font-medium text-gray-600 dark:text-gray-300">
                Hi, <span className="font-bold text-brand-400">{user.full_name || user.username}</span>
              </span>
              <button 
                onClick={onLogout}
                className="flex items-center gap-1 text-xs md:text-sm font-semibold px-2.5 py-1.5 rounded-lg border border-red-500/30 text-red-500 hover:bg-red-550/10 transition"
              >
                <LogOut size={14} /> <span className="hidden sm:inline">Sign Out</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2.5 md:gap-3">
              <Link 
                to="/login" 
                className="text-xs md:text-sm font-medium hover:text-brand-500 transition"
              >
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="text-xs md:text-sm font-semibold px-3 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-white shadow-lg shadow-brand-500/25 transition"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
};

// ==========================================
// Landing Page Component
// ==========================================
const LandingPage = () => {
  return (
    <div className="max-w-7xl mx-auto p-6 py-12 space-y-20">
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 text-xs font-semibold">
          <Cpu size={14} /> Powered by Gemini 2.5 Flash
        </div>
        
        <h1 className="text-5xl md:text-6xl font-black tracking-tight leading-none">
          Talk to Your IPL Data in{' '}
          <span className="bg-gradient-to-r from-brand-400 to-indigo-400 bg-clip-text text-transparent">
            Plain English
          </span>
        </h1>
        
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Transform your natural language questions into secure, optimized SQL queries automatically. Execute them instantly and visualize insights with interactive dashboards.
        </p>

        <div className="flex justify-center gap-4 pt-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold shadow-lg shadow-brand-500/25 transition"
          >
            Enter Dashboard <ChevronRight size={18} />
          </Link>
          
          <a
            href="#features"
            className="px-6 py-3 rounded-xl bg-gray-200 dark:bg-dark-muted hover:bg-gray-300 dark:hover:bg-gray-700 font-semibold transition"
          >
            Learn More
          </a>
        </div>
      </div>

      {/* Stats Mock Widget */}
      <div className="glass dark:bg-dark-paper/50 rounded-2xl p-6 glow-brand max-w-4xl mx-auto border border-gray-200 dark:border-gray-800 space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 pb-4">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
            <span className="w-3 h-3 rounded-full bg-green-500"></span>
          </div>
          <span className="text-xs text-gray-400 font-mono">NL-to-SQL Query Runner</span>
        </div>
        
        <div className="space-y-4">
          <div className="flex gap-3">
            <div className="bg-brand-500/10 text-brand-400 p-2 rounded-lg h-fit">
              <Terminal size={18} />
            </div>
            <div className="space-y-1 w-full">
              <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Input Question</p>
              <div className="bg-gray-100 dark:bg-dark-muted p-3 rounded-lg text-sm font-medium font-mono text-brand-400">
                "Show Virat Kohli's average against spin in IPL 2024"
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="bg-green-500/10 text-green-400 p-2 rounded-lg h-fit">
              <Play size={18} />
            </div>
            <div className="space-y-1 w-full">
              <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Generated SQL (Validated & Read-Only)</p>
              <pre className="bg-gray-900 text-green-400 p-4 rounded-lg text-xs overflow-x-auto font-mono">
{`SELECT 
  AVG(b.batter_runs) * 100 AS strike_rate,
  SUM(b.batter_runs) / COUNT(CASE WHEN b.is_wicket = 1 THEN 1 END) AS batting_average
FROM ball_by_ball b
JOIN ipl_match m ON b.match_id = m.match_id
WHERE b.batter = 'V Kohli' 
  AND b.bowler_type LIKE '%spin%' 
  AND m.season = '2024';`}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* Feature grid */}
      <div id="features" className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl space-y-4">
          <div className="p-3 bg-brand-500/10 text-brand-400 rounded-xl w-fit">
            <Shield size={24} />
          </div>
          <h3 className="font-bold text-lg">SQL Sandbox Security</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Queries are validated using AST parsing. Only SELECT statements can run against a restricted read-only MySQL database role.
          </p>
        </div>

        <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl space-y-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl w-fit">
            <TrendingUp size={24} />
          </div>
          <h3 className="font-bold text-lg">Smart Chart Recommendation</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            AI automatically recommends the most appropriate visualization type (Bar, Line, Radar, Area) based on the resulting query dataset.
          </p>
        </div>

        <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl space-y-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl w-fit">
            <Layers size={24} />
          </div>
          <h3 className="font-bold text-lg">Self-Reflecting Repair</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            If a query fails to run, the system uses a feedback loop to automatically diagnose MySQL errors and repair the SQL structure.
          </p>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// Authentication: Login Page
// ==========================================
const LoginPage = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await axios.post('/api/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      localStorage.setItem('cricsql_token', response.data.access_token);
      onLoginSuccess();
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Incorrect username or password. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="px-4 py-4 w-full">
      <div className="max-w-md mx-auto my-8 md:my-16 p-6 md:p-8 bg-white dark:bg-dark-paper rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800">
        <h2 className="text-3xl font-extrabold mb-2 text-center bg-gradient-to-r from-brand-400 to-indigo-400 bg-clip-text text-transparent">Sign In</h2>
        <p className="text-gray-500 dark:text-gray-400 text-sm text-center mb-6">Enter your credentials to access CricSQL analytics dashboard</p>

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 text-red-550 rounded-xl text-sm flex gap-2 items-center">
            <AlertTriangle size={16} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Username</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="e.g. admin"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="••••••••"
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold shadow-lg shadow-brand-500/25 transition flex items-center justify-center gap-2"
          >
            {loading ? 'Authenticating...' : 'Sign In'} <ArrowRight size={18} />
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          Don't have an account?{' '}
          <Link to="/register" className="text-brand-400 hover:underline font-semibold">
            Create account
          </Link>
        </p>
      </div>
    </div>
  );
};

// ==========================================
// Authentication: Register Page
// ==========================================
const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await axios.post('/api/auth/register', {
        username,
        email,
        password,
        full_name: fullName || null
      });

      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Try a different username/email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="px-4 py-4 w-full">
      <div className="max-w-md mx-auto my-8 md:my-16 p-6 md:p-8 bg-white dark:bg-dark-paper rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800">
        <h2 className="text-3xl font-extrabold mb-2 text-center bg-gradient-to-r from-brand-400 to-indigo-400 bg-clip-text text-transparent">Get Started</h2>
        <p className="text-gray-500 dark:text-gray-400 text-sm text-center mb-6">Create a free local account to get started with analytics</p>

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 text-red-550 rounded-xl text-sm flex gap-2 items-center">
            <AlertTriangle size={16} />
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-500/10 border border-green-500/30 text-green-400 rounded-xl text-sm flex gap-2 items-center">
            <CheckCircle size={16} />
            Registration successful! Redirecting to login...
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Full Name</label>
            <input 
              type="text" 
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="e.g. Sanjay Thomas"
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Username *</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="e.g. sanjay12"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Email Address *</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="sanjay@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Password * (Min 6 chars)</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 font-medium"
              placeholder="••••••••"
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading || success}
            className="w-full py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold shadow-lg shadow-brand-500/25 transition flex items-center justify-center gap-2"
          >
            {loading ? 'Creating account...' : 'Create Account'} <ArrowRight size={18} />
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          Already have an account?{' '}
          <Link to="/login" className="text-brand-400 hover:underline font-semibold">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
};

// ==========================================
// Interactive Chart Visualizer
// ==========================================
const DynamicChart = ({ recommendation, data }) => {
  if (!recommendation || !data || data.length === 0) return null;
  const { type, x_axis, y_axis, title } = recommendation;

  // Render proper chart based on type
  const renderChart = () => {
    switch (type.toLowerCase()) {
      case 'bar':
        return (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a3556" opacity={0.2} />
            <XAxis dataKey={x_axis} stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#151b2c', border: '1px solid #1e2640', borderRadius: '8px' }} 
              labelClassName="font-bold text-gray-150"
            />
            <Legend />
            <Bar dataKey={y_axis} fill="#5673ff" radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        );
      case 'line':
        return (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a3556" opacity={0.2} />
            <XAxis dataKey={x_axis} stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
            <Tooltip contentStyle={{ backgroundColor: '#151b2c', border: '1px solid #1e2640', borderRadius: '8px' }} />
            <Legend />
            <Line type="monotone" dataKey={y_axis} stroke="#5673ff" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 7 }} />
          </LineChart>
        );
      case 'area':
        return (
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#5673ff" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#5673ff" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a3556" opacity={0.2} />
            <XAxis dataKey={x_axis} stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
            <Tooltip contentStyle={{ backgroundColor: '#151b2c', border: '1px solid #1e2640', borderRadius: '8px' }} />
            <Legend />
            <Area type="monotone" dataKey={y_axis} stroke="#5673ff" fillOpacity={1} fill="url(#colorArea)" strokeWidth={2.5} />
          </AreaChart>
        );
      case 'pie':
        return (
          <PieChart>
            <Tooltip contentStyle={{ backgroundColor: '#151b2c', border: '1px solid #1e2640', borderRadius: '8px' }} />
            <Legend layout="horizontal" verticalAlign="bottom" align="center" />
            <Pie
              data={data}
              cx="50%"
              cy="45%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={95}
              fill="#5673ff"
              dataKey={y_axis}
              nameKey={x_axis}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        );
      case 'radar':
        return (
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
            <PolarGrid stroke="#2a3556" opacity={0.2} />
            <PolarAngleAxis dataKey={x_axis} stroke="#94a3b8" fontSize={10} />
            <PolarRadiusAxis stroke="#94a3b8" fontSize={9} />
            <Radar name={title} dataKey={y_axis} stroke="#5673ff" fill="#5673ff" fillOpacity={0.5} />
            <Tooltip contentStyle={{ backgroundColor: '#151b2c', border: '1px solid #1e2640', borderRadius: '8px' }} />
          </RadarChart>
        );
      default:
        return (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <TrendingUp size={36} className="mb-2" />
            <span className="text-sm">Table visualization recommended</span>
          </div>
        );
    }
  };

  return (
    <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl glow-brand flex flex-col h-full min-h-[350px]">
      <h3 className="text-md font-bold mb-4 flex items-center gap-2 border-b border-gray-150 dark:border-gray-800 pb-2">
        <TrendingUp size={18} className="text-brand-400" />
        {title || 'Query Visualization'}
        <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-550/20 font-mono capitalize ml-auto">
          {type}
        </span>
      </h3>
      <div className="flex-1 w-full min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// ==========================================
// Dashboard Component
// ==========================================
const Dashboard = ({ user }) => {
  const [activeTab, setActiveTab] = useState('console'); // console, history, saved
  const [nlQuery, setNlQuery] = useState('');
  
  // Running query state
  const [running, setRunning] = useState(false);
  const [runStage, setRunStage] = useState(''); // translating, executing, summarizing
  const [response, setResponse] = useState(null);
  
  // Modal save query state
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [saveTitle, setSaveTitle] = useState('');
  const [saveDesc, setSaveDesc] = useState('');
  const [saveLoading, setSaveLoading] = useState(false);
  
  // Lists
  const [historyList, setHistoryList] = useState([]);
  const [savedList, setSavedList] = useState([]);
  
  // Clipboard copied status
  const [copied, setCopied] = useState(false);
  
  // Suggested Questions
  const SUGGESTIONS = [
    "Show Virat Kohli's average against spin in IPL 2024",
    "List the top 5 batsmen with the most runs in the 2024 season",
    "What is the win percentage of teams winning the toss and choosing to bat first?",
    "Show the average runs scored per match at M Chinnaswamy Stadium compared to Wankhede Stadium"
  ];

  // Load history & saved queries
  const fetchHistory = async () => {
    try {
      const res = await axios.get('/api/analytics/history?limit=30', { headers: getAuthHeaders() });
      setHistoryList(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchSaved = async () => {
    try {
      const res = await axios.get('/api/analytics/saved', { headers: getAuthHeaders() });
      setSavedList(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchHistory();
    fetchSaved();
  }, [activeTab]);

  // Execute Query
  const runQuery = async (queryText) => {
    if (!queryText || queryText.trim().length < 5) return;
    setNlQuery(queryText);
    setRunning(true);
    setResponse(null);
    
    // Simulate steps for beautiful UI transitions
    setRunStage('Translating English to MySQL SQL via Gemini...');
    setTimeout(() => {
      setRunStage('Validating query safety (SELECT rules check)...');
      setTimeout(() => {
        setRunStage('Executing query on local MySQL db...');
      }, 700);
    }, 700);

    try {
      const res = await axios.post('/api/analytics/query', { query: queryText }, { headers: getAuthHeaders() });
      setResponse(res.data);
    } catch (err) {
      setResponse({
        success: false,
        error: err.response?.data?.detail || 'An error occurred during query execution. Check backend logs.'
      });
    } finally {
      setRunning(false);
      fetchHistory(); // Refresh history list
    }
  };

  // Copy SQL to clipboard
  const handleCopySql = () => {
    if (!response || !response.sql) return;
    navigator.clipboard.writeText(response.sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Export Results as CSV
  const handleExportCsv = () => {
    if (!response || !response.rows || response.rows.length === 0) return;
    const cols = response.columns;
    const csvContent = [
      cols.join(','),
      ...response.rows.map(row => 
        cols.map(c => {
          let val = row[c] === null ? '' : String(row[c]);
          if (val.includes(',') || val.includes('"') || val.includes('\n')) {
            val = `"${val.replace(/"/g, '""')}"`;
          }
          return val;
        }).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `cricsql_export_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Save Query to library
  const handleSaveQuery = async (e) => {
    e.preventDefault();
    if (!response || !saveTitle) return;
    setSaveLoading(true);

    try {
      await axios.post('/api/analytics/saved', {
        title: saveTitle,
        description: saveDesc || null,
        natural_language_query: response.query,
        generated_sql: response.sql
      }, { headers: getAuthHeaders() });
      
      setShowSaveModal(false);
      setSaveTitle('');
      setSaveDesc('');
      fetchSaved();
    } catch (e) {
      alert('Failed to save query. Please check fields.');
    } finally {
      setSaveLoading(false);
    }
  };

  // Delete saved query
  const handleDeleteSaved = async (queryId) => {
    if (!confirm('Are you sure you want to delete this saved query?')) return;
    try {
      await axios.delete(`/api/analytics/saved/${queryId}`, { headers: getAuthHeaders() });
      fetchSaved();
    } catch (e) {
      alert('Could not delete query.');
    }
  };

  // Delete query history item
  const handleDeleteHistoryItem = async (historyId) => {
    if (!confirm('Are you sure you want to delete this query from history?')) return;
    try {
      await axios.delete(`/api/analytics/history/${historyId}`, { headers: getAuthHeaders() });
      fetchHistory();
    } catch (e) {
      alert('Could not delete history item.');
    }
  };

  // Clear all query history
  const handleClearAllHistory = async () => {
    if (!confirm('Are you sure you want to delete your entire search history? This cannot be undone.')) return;
    try {
      await axios.delete('/api/analytics/history', { headers: getAuthHeaders() });
      fetchHistory();
    } catch (e) {
      alert('Could not clear history.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-6 flex flex-col md:flex-row gap-6 min-h-[calc(100vh-80px)]">
      {/* Sidebar/Tab navigation */}
      <div className="w-full md:w-64 shrink-0 flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0 scrollbar-none border-b md:border-b-0 border-gray-200 dark:border-gray-800">
        <button
          onClick={() => setActiveTab('console')}
          className={`flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl font-bold text-xs md:text-sm transition whitespace-nowrap shrink-0 justify-center md:justify-start flex-1 md:flex-initial ${
            activeTab === 'console' 
              ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/20' 
              : 'hover:bg-gray-100 dark:hover:bg-dark-muted text-gray-500 dark:text-gray-400'
          }`}
        >
          <Terminal size={16} className="shrink-0" /> <span>Console</span>
        </button>

        <button
          onClick={() => setActiveTab('history')}
          className={`flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl font-bold text-xs md:text-sm transition whitespace-nowrap shrink-0 justify-center md:justify-start flex-1 md:flex-initial ${
            activeTab === 'history' 
              ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/20' 
              : 'hover:bg-gray-100 dark:hover:bg-dark-muted text-gray-500 dark:text-gray-400'
          }`}
        >
          <Clock size={16} className="shrink-0" /> <span>History</span>
        </button>

        <button
          onClick={() => setActiveTab('saved')}
          className={`flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl font-bold text-xs md:text-sm transition whitespace-nowrap shrink-0 justify-center md:justify-start flex-1 md:flex-initial ${
            activeTab === 'saved' 
              ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/20' 
              : 'hover:bg-gray-100 dark:hover:bg-dark-muted text-gray-500 dark:text-gray-400'
          }`}
        >
          <Bookmark size={16} className="shrink-0" /> <span>Library</span>
        </button>
      </div>

      {/* Main Panel */}
      <div className="flex-1 min-w-0 space-y-6">
        <AnimatePresence mode="wait">
          {activeTab === 'console' && (
            <motion.div
              key="console"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              {/* Question Input Card */}
              <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl shadow-md space-y-4">
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <Cpu size={16} className="text-brand-400" />
                  <span>Ask a question about IPL matches, player performances, ball by ball actions, or team analytics.</span>
                </div>
                
                <div className="relative">
                  <textarea
                    value={nlQuery}
                    onChange={(e) => setNlQuery(e.target.value)}
                    placeholder='e.g. "Which batsman scored the most runs in IPL 2024?" or "Show average runs scored per match at Eden Gardens"'
                    className="w-full min-h-[100px] pl-4 pr-12 py-3.5 rounded-2xl bg-gray-50 dark:bg-dark-muted border border-slate-200 dark:border-slate-800 focus:outline-none focus:border-brand-500 focus:ring-4 focus:ring-brand-500/10 dark:focus:ring-brand-400/10 font-medium text-md text-slate-800 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 transition duration-200"
                  />
                  <button
                    onClick={() => runQuery(nlQuery)}
                    disabled={running || !nlQuery.trim()}
                    className="absolute right-3 bottom-4 p-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white shadow-lg shadow-brand-500/20 transition disabled:opacity-50"
                    aria-label="Run Question"
                  >
                    <Play size={18} fill="white" />
                  </button>
                </div>

                {/* Suggested Questions */}
                <div className="space-y-2">
                  <span className="text-xs uppercase font-bold text-gray-400 tracking-wider">Try these suggested queries:</span>
                  <div className="flex flex-wrap gap-2">
                    {SUGGESTIONS.map((s, idx) => (
                      <button
                        key={idx}
                        onClick={() => runQuery(s)}
                        disabled={running}
                        className="text-xs px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-dark-muted hover:bg-brand-500/10 hover:border-brand-500/35 transition text-left"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Running Status Screen */}
              {running && (
                <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-8 rounded-2xl shadow-md text-center space-y-4">
                  <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                  <h4 className="font-bold text-lg">AI Analytics Engine Working...</h4>
                  <p className="text-sm text-gray-400 max-w-sm mx-auto font-mono bg-dark-muted py-1.5 px-3 rounded-lg border border-gray-700">{runStage}</p>
                </div>
              )}

              {/* Response results area */}
              {response && (
                <div className="space-y-6">
                  {response.success ? (
                    <>
                      {/* Commentary and Charts Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Gemini Insights Commentary */}
                        <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl shadow-md flex flex-col justify-between min-h-[350px]">
                          <div>
                            <h3 className="text-md font-bold mb-4 flex items-center gap-2 border-b border-gray-150 dark:border-gray-800 pb-2">
                              <Cpu size={18} className="text-brand-400" />
                              AI Insights & Commentary
                            </h3>
                            <p className="text-md leading-relaxed text-gray-700 dark:text-gray-300 font-medium italic">
                              "{response.explanation || 'No commentary generated.'}"
                            </p>
                          </div>
                          <div className="flex gap-2 pt-6 border-t border-gray-150 dark:border-gray-800 mt-6">
                            <button
                              onClick={() => setShowSaveModal(true)}
                              className="flex items-center gap-2 text-xs font-bold px-3 py-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 hover:bg-indigo-550/20 transition"
                            >
                              <PlusCircle size={14} /> Save to Dashboard
                            </button>
                            <button
                              onClick={handleExportCsv}
                              className="flex items-center gap-2 text-xs font-bold px-3 py-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-550/20 transition"
                            >
                              <Download size={14} /> Export CSV
                            </button>
                          </div>
                        </div>

                        {/* Chart recommendation visualizer */}
                        {response.chart_recommendation && response.rows && response.rows.length > 0 ? (
                          <DynamicChart 
                            recommendation={response.chart_recommendation} 
                            data={response.rows} 
                          />
                        ) : (
                          <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl shadow-md flex flex-col items-center justify-center text-gray-400 text-center min-h-[300px]">
                            <TrendingUp size={36} className="mb-2 text-brand-400/50" />
                            <span className="text-sm font-semibold">Table Visualizer Mode</span>
                            <p className="text-xs text-gray-500 mt-1 max-w-[200px]">Results are best examined directly in the tabular format below.</p>
                          </div>
                        )}
                      </div>

                      {/* SQL Code Block */}
                      <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-6 rounded-2xl shadow-md space-y-3">
                        <div className="flex items-center justify-between border-b border-gray-150 dark:border-gray-800 pb-2">
                          <h4 className="text-sm font-bold flex items-center gap-2">
                            <Code size={16} className="text-green-400" /> Generated SQL Query
                          </h4>
                          <button
                            onClick={handleCopySql}
                            className="flex items-center gap-1.5 text-xs text-gray-450 hover:text-white bg-dark-muted px-2 py-1 rounded border border-gray-700 transition"
                          >
                            <Copy size={12} /> {copied ? 'Copied' : 'Copy'}
                          </button>
                        </div>
                        <pre className="bg-gray-900 text-green-400 p-4 rounded-xl text-xs overflow-x-auto font-mono leading-relaxed">
                          {response.sql}
                        </pre>
                      </div>

                      {/* Data table */}
                      <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 rounded-2xl shadow-md overflow-hidden">
                        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-dark-paper">
                          <h4 className="text-sm font-bold flex items-center gap-2">
                            <FileSpreadsheet size={16} className="text-brand-400" /> Data Table Results
                          </h4>
                          <span className="text-xs bg-brand-500/10 text-brand-400 px-2.5 py-0.5 rounded-full font-medium border border-brand-500/25">
                            {response.rows?.length || 0} rows found in {response.execution_time_ms || 0}ms
                          </span>
                        </div>
                        {response.rows && response.rows.length > 0 ? (
                          <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                              <thead>
                                <tr className="border-b border-gray-200 dark:border-gray-800 bg-gray-100/50 dark:bg-dark-muted/50">
                                  {response.columns.map((col, idx) => (
                                    <th key={idx} className="px-6 py-3.5 text-xs uppercase font-extrabold text-gray-455 tracking-wider">
                                      {col.replace(/_/g, ' ')}
                                    </th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody>
                                {response.rows.map((row, rIdx) => (
                                  <tr 
                                    key={rIdx} 
                                    className="border-b border-gray-150 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-dark-muted/30 transition text-sm font-medium"
                                  >
                                    {response.columns.map((col, cIdx) => (
                                      <td key={cIdx} className="px-6 py-3 text-gray-700 dark:text-gray-300">
                                        {row[col] === null ? '-' : String(row[col])}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        ) : (
                          <div className="p-8 text-center text-gray-500 dark:text-gray-400">
                            Query executed successfully but returned empty result set.
                          </div>
                        )}
                      </div>
                    </>
                  ) : (
                    /* Error State Card */
                    <div className="bg-red-500/5 border border-red-500/30 p-6 rounded-2xl shadow-md space-y-4">
                      <div className="flex gap-3 items-start">
                        <div className="p-2 bg-red-500/10 text-red-500 rounded-lg">
                          <AlertTriangle size={24} />
                        </div>
                        <div>
                          <h4 className="font-bold text-lg text-red-500">Query Failed to Execute</h4>
                          <p className="text-sm text-gray-400 mt-1">MySQL reported an error during query validation or execution.</p>
                        </div>
                      </div>
                      
                      <div className="bg-gray-900 border border-red-500/20 p-4 rounded-xl font-mono text-xs text-red-400 space-y-2">
                        <p className="font-semibold text-gray-400 uppercase tracking-wide border-b border-gray-800 pb-1">Error Message</p>
                        <p>{response.error}</p>
                      </div>

                      {response.sql && (
                        <div className="space-y-2">
                          <p className="text-xs uppercase font-bold text-gray-450 tracking-wider">Generated SQL Query</p>
                          <pre className="bg-gray-900 text-gray-450 p-4 rounded-xl text-xs overflow-x-auto font-mono">
                            {response.sql}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'history' && (
            <motion.div
              key="history"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
              className="space-y-4"
            >
              <div className="flex justify-between items-center pb-2">
                <h3 className="text-xl font-extrabold flex items-center gap-2">
                  <Clock className="text-brand-400" /> Previous Queries
                </h3>
                {historyList.length > 0 && (
                  <button
                    onClick={handleClearAllHistory}
                    className="flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-lg border border-red-500/30 text-red-550 hover:bg-red-550/10 transition"
                  >
                    <Trash2 size={12} /> Clear All History
                  </button>
                )}
              </div>
              
              {historyList.length > 0 ? (
                <div className="space-y-3">
                  {historyList.map((h, index) => (
                    <div 
                      key={index} 
                      className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-5 rounded-2xl flex flex-col md:flex-row justify-between md:items-center gap-4 hover:border-brand-500/40 transition"
                    >
                      <div className="space-y-1.5">
                        <div className="flex items-center gap-2">
                          {h.is_success ? (
                            <span className="text-emerald-400 bg-emerald-500/10 text-xs px-2 py-0.5 rounded-full border border-emerald-500/20 flex items-center gap-1 font-bold">
                              <CheckCircle size={10} /> Success
                            </span>
                          ) : (
                            <span className="text-red-400 bg-red-500/10 text-xs px-2 py-0.5 rounded-full border border-red-550/20 flex items-center gap-1 font-bold">
                              <AlertTriangle size={10} /> Failed
                            </span>
                          )}
                          <span className="text-xs text-gray-500 font-mono">
                            {new Date(h.created_at).toLocaleString()}
                          </span>
                          <span className="text-xs text-gray-500 font-mono">
                            {h.execution_time_ms || 0}ms
                          </span>
                        </div>
                        <p className="font-bold text-md text-gray-800 dark:text-gray-150">"{h.query}"</p>
                        <details className="text-xs text-gray-400 cursor-pointer">
                          <summary className="hover:text-white transition font-bold font-mono">View SQL Code</summary>
                          <pre className="mt-2 bg-gray-900 text-green-400 p-3 rounded-lg font-mono overflow-x-auto text-[11px] leading-relaxed">
                            {h.sql}
                          </pre>
                        </details>
                      </div>

                      <div className="flex items-center gap-2 shrink-0 self-end md:self-auto">
                        <button
                          onClick={() => {
                            setActiveTab('console');
                            runQuery(h.query);
                          }}
                          className="flex items-center justify-center gap-1 text-xs font-bold px-4 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white shadow-md shadow-brand-500/15 transition h-fit"
                        >
                          Run Console <Play size={12} fill="white" />
                        </button>
                        <button
                          onClick={() => handleDeleteHistoryItem(h.id)}
                          className="p-2 text-gray-400 hover:text-red-500 border border-gray-200 dark:border-gray-850 hover:border-red-500/35 bg-gray-50 dark:bg-dark-muted rounded-xl transition"
                          title="Delete history item"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-12 rounded-2xl text-center text-gray-500">
                  You have not run any analytics queries yet.
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'saved' && (
            <motion.div
              key="saved"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
              className="space-y-4"
            >
              <h3 className="text-xl font-extrabold flex items-center gap-2">
                <Bookmark className="text-brand-400" /> Saved Queries
              </h3>

              {savedList.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {savedList.map((s, index) => (
                    <div 
                      key={index} 
                      className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-5 rounded-2xl flex flex-col justify-between hover:border-indigo-500/40 transition"
                    >
                      <div className="space-y-2">
                        <div className="flex justify-between items-start gap-2">
                          <h4 className="font-extrabold text-md text-brand-400">{s.title}</h4>
                          <button
                            onClick={() => handleDeleteSaved(s.id)}
                            className="p-1 text-gray-400 hover:text-red-500 transition"
                            aria-label="Delete saved query"
                          >
                            <X size={16} />
                          </button>
                        </div>
                        {s.description && (
                          <p className="text-xs text-gray-400 leading-relaxed">{s.description}</p>
                        )}
                        <div className="bg-gray-50 dark:bg-dark-muted p-3 rounded-lg border border-gray-250 dark:border-gray-800 text-xs font-mono italic text-gray-600 dark:text-gray-300">
                          "{s.natural_language_query}"
                        </div>
                      </div>

                      <div className="flex justify-between items-center gap-2 mt-4 pt-4 border-t border-gray-150 dark:border-gray-800">
                        <span className="text-[10px] text-gray-500 font-mono">
                          Saved: {new Date(s.created_at).toLocaleDateString()}
                        </span>
                        <button
                          onClick={() => {
                            setActiveTab('console');
                            runQuery(s.natural_language_query);
                          }}
                          className="flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-lg bg-brand-500 hover:bg-brand-600 text-white shadow-md shadow-brand-500/10 transition"
                        >
                          Run Query <Play size={10} fill="white" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-white dark:bg-dark-paper border border-gray-200 dark:border-gray-800 p-12 rounded-2xl text-center text-gray-500">
                  Your saved library is empty. Run queries in the Console and click "Save to Dashboard".
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Save Query Modal Dialog */}
      {showSaveModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div 
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-full max-w-md bg-white dark:bg-dark-paper border border-gray-250 dark:border-gray-800 p-6 rounded-2xl shadow-2xl space-y-4"
          >
            <div className="flex justify-between items-center border-b border-gray-150 dark:border-gray-800 pb-2">
              <h3 className="font-extrabold text-lg text-brand-400">Save Query to Library</h3>
              <button 
                onClick={() => setShowSaveModal(false)}
                className="text-gray-400 hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSaveQuery} className="space-y-4">
              <div>
                <label className="block text-xs uppercase font-bold text-gray-400 mb-1">Title *</label>
                <input
                  type="text"
                  value={saveTitle}
                  onChange={(e) => setSaveTitle(e.target.value)}
                  placeholder="e.g. Virat Kohli 2024 Spin Stats"
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 text-sm font-medium"
                  required
                />
              </div>

              <div>
                <label className="block text-xs uppercase font-bold text-gray-400 mb-1">Description (Optional)</label>
                <textarea
                  value={saveDesc}
                  onChange={(e) => setSaveDesc(e.target.value)}
                  placeholder="Summarize what insights this query shows..."
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-dark-muted border border-gray-200 dark:border-gray-700 focus:outline-none focus:border-brand-500 text-sm font-medium min-h-[60px]"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowSaveModal(false)}
                  className="px-4 py-2 rounded-lg bg-gray-100 dark:bg-dark-muted hover:bg-gray-200 dark:hover:bg-gray-750 transition text-xs font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saveLoading || !saveTitle}
                  className="px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-white font-bold transition text-xs shadow-md shadow-brand-500/10"
                >
                  {saveLoading ? 'Saving...' : 'Save Query'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
};

// ==========================================
// Main Routing and Auth State Component
// ==========================================
export default function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Sync dark mode class
  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [darkMode]);

  // Load user profile on mount
  const checkAuth = async () => {
    const token = localStorage.getItem('cricsql_token');
    if (!token) {
      setUser(null);
      setAuthLoading(false);
      return;
    }

    try {
      const response = await axios.get('/api/auth/profile', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUser(response.data);
    } catch (e) {
      localStorage.removeItem('cricsql_token');
      setUser(null);
    } finally {
      setAuthLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('cricsql_token');
    setUser(null);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-dark flex flex-col items-center justify-center text-white space-y-4">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm text-gray-400 font-medium">Loading CricSQL platform...</p>
      </div>
    );
  }

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout darkMode={darkMode} setDarkMode={setDarkMode} user={user} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={
            user ? <Navigate to="/dashboard" replace /> : <LoginPage onLoginSuccess={checkAuth} />
          } />
          <Route path="/register" element={
            user ? <Navigate to="/dashboard" replace /> : <RegisterPage />
          } />
          <Route path="/dashboard" element={
            user ? <Dashboard user={user} /> : <Navigate to="/login" replace />
          } />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}
