import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Chip,
  Stack,
  Alert,
  CircularProgress,
  Fade,
  InputAdornment,
  IconButton,
  Avatar
} from '@mui/material';
import {
  Send as SendIcon,
  Psychology as PsychologyIcon,
  DataObject as DataObjectIcon,
  Add as AddIcon,
  AttachFile as AttachFileIcon,
  InsertDriveFile as FileIcon,
  Insights as InsightsIcon
} from '@mui/icons-material';

const API_URL = 'http://localhost:8000';

// Create a modern, minimal dark theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#818cf8',
      light: '#a5b4fc',
      dark: '#6366f1',
    },
    secondary: {
      main: '#a78bfa',
    },
    background: {
      default: '#0f172a',
      paper: '#1e293b',
    },
    text: {
      primary: '#f1f5f9',
      secondary: '#94a3b8',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadStatus({ type: 'info', message: `Uploading ${file.name}...` });
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData);
      setUploadStatus({
        type: 'success',
        message: `✅ Document processed! ${response.data.chunks_created} chunks stored in vector database.`,
      });

      setMessages(prev => [...prev, {
        type: 'system',
        text: `Document "${file.name}" uploaded and processed through RAG pipeline. Ready for queries!`,
        timestamp: new Date(),
      }]);

      setTimeout(() => setUploadStatus(null), 5000);
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: `❌ Error: ${error.response?.data?.detail || error.message}`,
      });
    }
  };

  // Handle query
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');

    setMessages(prev => [...prev, {
      type: 'user',
      text: userMessage,
      timestamp: new Date(),
    }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/query`, {
        query: userMessage
      });

      setMessages(prev => [...prev, {
        type: 'agent',
        text: response.data.answer,
        tool: response.data.tool_used,
        time: response.data.execution_time_ms,
        timestamp: new Date(),
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'agent',
        text: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileIconClick = () => {
    fileInputRef.current?.click();
  };

  const getToolIcon = (toolName) => {
    switch (toolName) {
      case 'qa_tool':
        return <PsychologyIcon sx={{ fontSize: 16 }} />;
      case 'insights_tool':
        return <InsightsIcon sx={{ fontSize: 16 }} />;
      case 'extract_tool':
        return <DataObjectIcon sx={{ fontSize: 16 }} />;
      default:
        return null;
    }
  };

  const getToolLabel = (toolName) => {
    switch (toolName) {
      case 'qa_tool':
        return 'Q&A';
      case 'insights_tool':
        return 'Insights';
      case 'extract_tool':
        return 'Extract';
      default:
        return toolName;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          backgroundColor: '#1e1e1e',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            px: 3,
            py: 2,
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 600, background: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Market Analyst
          </Typography>
          <Avatar sx={{ width: 32, height: 32, background: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)' }}>
            M
          </Avatar>
        </Box>

        {/* Main Content */}
        <Box
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: messages.length === 0 ? 'center' : 'flex-start',
            maxWidth: '900px',
            width: '100%',
            mx: 'auto',
            px: 3,
            py: messages.length === 0 ? 0 : 4,
            overflowY: 'auto',
          }}
        >
          {messages.length === 0 ? (
            <>
              {/* Centered greeting and input */}
              <Box sx={{ textAlign: 'center', width: '100%', maxWidth: '680px' }}>
                <Typography
                  variant="h3"
                  sx={{
                    mb: 6,
                    fontWeight: 400,
                    background: 'linear-gradient(135deg, #a5b4fc 0%, #c4b5fd 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                  }}
                >
                  Hello
                </Typography>

                {/* Hidden file input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />

                {/* Large input field */}
                <Paper
                  elevation={0}
                  sx={{
                    mb: 4,
                    backgroundColor: '#2d2d2d',
                    borderRadius: '28px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    '&:hover': {
                      backgroundColor: '#323232',
                    },
                  }}
                >
                  <TextField
                    fullWidth
                    multiline
                    maxRows={4}
                    placeholder="Ask Market Analyst"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                    variant="standard"
                    InputProps={{
                      disableUnderline: true,
                      startAdornment: (
                        <InputAdornment position="start" sx={{ ml: 2 }}>
                          <IconButton
                            onClick={handleFileIconClick}
                            disabled={isLoading}
                            sx={{
                              color: 'text.secondary',
                              '&:hover': {
                                backgroundColor: 'rgba(129, 140, 248, 0.1)',
                              },
                            }}
                          >
                            <AddIcon />
                          </IconButton>
                        </InputAdornment>
                      ),
                      endAdornment: inputMessage.trim() && (
                        <InputAdornment position="end" sx={{ mr: 1 }}>
                          <IconButton
                            onClick={handleSendMessage}
                            disabled={isLoading || !inputMessage.trim()}
                            sx={{
                              color: 'primary.main',
                              '&:hover': {
                                backgroundColor: 'rgba(129, 140, 248, 0.1)',
                              },
                            }}
                          >
                            <SendIcon />
                          </IconButton>
                        </InputAdornment>
                      ),
                      sx: {
                        px: 1,
                        py: 1.5,
                        fontSize: '16px',
                      },
                    }}
                  />
                </Paper>

                {/* Suggestion chips */}
                <Stack direction="row" spacing={2} sx={{ justifyContent: 'center', flexWrap: 'wrap', gap: 2 }}>
                  <Chip
                    icon={<AttachFileIcon />}
                    label="Upload Document"
                    onClick={handleFileIconClick}
                    sx={{
                      backgroundColor: '#2d2d2d',
                      color: 'text.primary',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      '&:hover': {
                        backgroundColor: '#323232',
                      },
                    }}
                  />
                  <Chip
                    icon={<PsychologyIcon />}
                    label="Q&A Analysis"
                    sx={{
                      backgroundColor: '#2d2d2d',
                      color: 'text.primary',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      '&:hover': {
                        backgroundColor: '#323232',
                      },
                    }}
                  />
                  <Chip
                    icon={<InsightsIcon />}
                    label="Strategic Insights"
                    sx={{
                      backgroundColor: '#2d2d2d',
                      color: 'text.primary',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      '&:hover': {
                        backgroundColor: '#323232',
                      },
                    }}
                  />
                  <Chip
                    icon={<DataObjectIcon />}
                    label="Extract Data"
                    sx={{
                      backgroundColor: '#2d2d2d',
                      color: 'text.primary',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      '&:hover': {
                        backgroundColor: '#323232',
                      },
                    }}
                  />
                </Stack>

                {/* Upload status */}
                {uploadStatus && (
                  <Fade in={true}>
                    <Alert
                      severity={uploadStatus.type === 'error' ? 'error' : uploadStatus.type === 'success' ? 'success' : 'info'}
                      sx={{ mt: 3 }}
                      onClose={() => setUploadStatus(null)}
                    >
                      {uploadStatus.message}
                    </Alert>
                  </Fade>
                )}
              </Box>
            </>
          ) : (
            <>
              {/* Chat messages */}
              <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 3 }}>
                {messages.map((msg, idx) => (
                  <Fade in={true} key={idx}>
                    <Box>
                      {msg.type === 'user' ? (
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
                          <Paper
                            elevation={0}
                            sx={{
                              px: 3,
                              py: 2,
                              backgroundColor: '#2d2d2d',
                              maxWidth: '80%',
                              borderRadius: '20px',
                            }}
                          >
                            <Typography sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                              {msg.text}
                            </Typography>
                          </Paper>
                        </Box>
                      ) : msg.type === 'system' ? (
                        <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                          <Chip
                            icon={<FileIcon />}
                            label={msg.text}
                            sx={{
                              backgroundColor: 'rgba(129, 140, 248, 0.1)',
                              color: 'primary.light',
                              borderRadius: '16px',
                            }}
                          />
                        </Box>
                      ) : (
                        <Box sx={{ display: 'flex', gap: 2 }}>
                          <Avatar
                            sx={{
                              width: 32,
                              height: 32,
                              background: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)',
                              mt: 0.5,
                            }}
                          >
                            M
                          </Avatar>
                          <Box sx={{ flex: 1 }}>
                            <Paper
                              elevation={0}
                              sx={{
                                px: 3,
                                py: 2,
                                backgroundColor: '#2d2d2d',
                                borderRadius: '20px',
                              }}
                            >
                              <Typography sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', mb: msg.tool ? 1.5 : 0 }}>
                                {msg.text}
                              </Typography>
                              {msg.tool && (
                                <Stack direction="row" spacing={1} alignItems="center">
                                  <Chip
                                    icon={getToolIcon(msg.tool)}
                                    label={getToolLabel(msg.tool)}
                                    size="small"
                                    sx={{
                                      backgroundColor: 'rgba(129, 140, 248, 0.2)',
                                      color: 'primary.light',
                                      height: 24,
                                      fontSize: '0.75rem',
                                    }}
                                  />
                                  <Typography variant="caption" color="text.secondary">
                                    {msg.time}ms
                                  </Typography>
                                </Stack>
                              )}
                            </Paper>
                          </Box>
                        </Box>
                      )}
                    </Box>
                  </Fade>
                ))}
                {isLoading && (
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Avatar
                      sx={{
                        width: 32,
                        height: 32,
                        background: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)',
                        mt: 0.5,
                      }}
                    >
                      M
                    </Avatar>
                    <Paper
                      elevation={0}
                      sx={{
                        px: 3,
                        py: 2,
                        backgroundColor: '#2d2d2d',
                        borderRadius: '20px',
                        display: 'flex',
                        gap: 1,
                        alignItems: 'center',
                      }}
                    >
                      <CircularProgress size={16} />
                      <Typography variant="body2">Thinking...</Typography>
                    </Paper>
                  </Box>
                )}
                <div ref={messagesEndRef} />
              </Box>

              {/* Input at bottom when chat is active */}
              <Box
                sx={{
                  position: 'sticky',
                  bottom: 0,
                  width: '100%',
                  pt: 3,
                  pb: 2,
                  backgroundColor: '#1e1e1e',
                }}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />
                <Paper
                  elevation={0}
                  sx={{
                    backgroundColor: '#2d2d2d',
                    borderRadius: '28px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    '&:hover': {
                      backgroundColor: '#323232',
                    },
                  }}
                >
                  <TextField
                    fullWidth
                    multiline
                    maxRows={4}
                    placeholder="Ask a follow-up question..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                    variant="standard"
                    InputProps={{
                      disableUnderline: true,
                      startAdornment: (
                        <InputAdornment position="start" sx={{ ml: 2 }}>
                          <IconButton
                            onClick={handleFileIconClick}
                            disabled={isLoading}
                            sx={{
                              color: 'text.secondary',
                              '&:hover': {
                                backgroundColor: 'rgba(129, 140, 248, 0.1)',
                              },
                            }}
                          >
                            <AddIcon />
                          </IconButton>
                        </InputAdornment>
                      ),
                      endAdornment: inputMessage.trim() && (
                        <InputAdornment position="end" sx={{ mr: 1 }}>
                          <IconButton
                            onClick={handleSendMessage}
                            disabled={isLoading || !inputMessage.trim()}
                            sx={{
                              color: 'primary.main',
                              '&:hover': {
                                backgroundColor: 'rgba(129, 140, 248, 0.1)',
                              },
                            }}
                          >
                            <SendIcon />
                          </IconButton>
                        </InputAdornment>
                      ),
                      sx: {
                        px: 1,
                        py: 1.5,
                        fontSize: '16px',
                      },
                    }}
                  />
                </Paper>
              </Box>
            </>
          )}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
