import React, { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import  './Login.css'

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
       Finance Fusion 
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

export default function SignIn() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
   const navigate = useNavigate();
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const data = {
      username: username,
      password: password,
    };
    console.log(data);

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Successful login, now get the access token and store it
        const { access_token } = await response.json();
        console.log(access_token);
        sessionStorage.setItem('access_token', access_token);
        const fetchData = async () => {
          try {
            // Fetch data from your API endpoint
            const response = await fetch("http://127.0.0.1:5000/get-data",{
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${access_token}`,
              }});
            const jsonData = await response.json();
            console.log(jsonData)
          } catch (error) {
            console.log("Error fetching data:", error);
          }
        };
        fetchData();
        navigate('/dashboard');
      } else {
        // Handle login error
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };



  return (
    <ThemeProvider theme={defaultTheme}>
      <div className='main-container' >

      <Container className='signin-container' component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="User name"
              name="username"
              autoComplete="username"
              autoFocus
              onChange={(e) => setUsername(e.target.value)}
              />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              >
              Sign In
            </Button>
            </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
              </div>
    </ThemeProvider>
  );
}