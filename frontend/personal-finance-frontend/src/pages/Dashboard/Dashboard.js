import React, { useEffect, useState } from "react";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Badge from "@mui/material/Badge";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Bar from "./visualizations/bar.png";
import line_exp from "./visualizations/line_expense.png";
import line_income from "./visualizations/line_income.png";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";

import "./Dashboard.css";

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      Finance Fusion
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const defaultTheme = createTheme();

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch data from your API endpoint
      const accessToken = sessionStorage.getItem("access_token");
      const response = await fetch("http://127.0.0.1:5000/dashboard", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.log("Error fetching data:", error);
    }
  };
  console.log(data);

  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  const barImagePath = new URL(Bar, import.meta.url).pathname;
  const lineExpImagePath = new URL(line_exp, import.meta.url).pathname;
  const lineIncImagePath = new URL(line_income, import.meta.url).pathname;

  const ExceedBudgetTableComponent = () => {
    // Assuming exceededBudgetData and withinBudgetData are the provided data
    const exceededBudgetData = data.data.exceededBudget;

    return (
      <div>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Category</TableCell>
                <TableCell>Amount</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(exceededBudgetData).map(([category, amount]) => (
                <TableRow key={category}>
                  <TableCell>{category}</TableCell>
                  <TableCell>{amount}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    );
  };

  const TableComponent = () => {
    // Assuming spendingCategoriesData is the provided spending categories data
    const spendingCategoriesData = data.data.spendingCategories

    return (
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Category</TableCell>
              <TableCell>Amount</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(spendingCategoriesData).map(
              ([category, amount]) => (
                <TableRow key={category}>
                  <TableCell>{category}</TableCell>
                  <TableCell>{amount}</TableCell>
                </TableRow>
              )
            )}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  // Parse the JSON response and access the values
  const spendingCategories = JSON.parse(data.data.spending_categories);
  console.log(spendingCategories);

  // Integrate new bank form
  const [open, setOpen] = useState(false);
  const [bankName, setBankName] = useState("");
  const [accountNumber, setAccountNumber] = useState("");

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleBankNameChange = (event) => {
    setBankName(event.target.value);
  };

  const handleAccountNumberChange = (event) => {
    setAccountNumber(event.target.value);
  };

  const handleSubmit = () => {
    // Perform integration logic here
    submitFormData();
    handleClose();
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar position="absolute">
          <Toolbar
            sx={{
              pr: "24px", // keep right padding when drawer closed
            }}
          >
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Personal Finance Management Dashboard
            </Typography>
            <IconButton color="inherit">
              <Badge color="secondary">
                <AccountCircleIcon />
              </Badge>
            </IconButton>
          </Toolbar>
        </AppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              {/* Chart */}
              <Grid item xs={12} md={8} lg={9}>
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: 650,
                  }}
                >
                  <Typography variant="h3">Withdrawal vs deposits</Typography>
                  <img
                    src={barImagePath}
                    alt="Bar Chart"
                    className="chart-image"
                  />
                </Paper>
              </Grid>
              {/* Recent Deposits */}
              <Grid item xs={12} md={4} lg={3}>
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: 700,
                  }}
                >
                  <Typography component="h2">Current Balance</Typography>
                  <Typography component="p" variant="h4">
                    $
                    {data.data.balance.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </Typography>
                  <br />
                  <br />
                  <Typography component="h2">Account Numbers:</Typography>
                  <Typography component="p">
                    <br />
                    Primary Bank: 
                    {data.data.accounts[0]}
                  </Typography>
                  <Typography component="p">
                    Secondary Bank: 
                    {data.data.accounts[1]}
                    <br />
                  </Typography>
                  <Typography component="p">
                    Payment Processor: 
                    {data.data.accounts[2]}
                  </Typography>
                  <br /> <br />
                  <Typography component="h2">Debt to Income Ratio</Typography>
                  <Typography component="p" variant="h5">
                    {data.data.debt_to_income_ratio.toLocaleString(
                      undefined,
                      {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 6,
                      }
                    )}
                  </Typography>
                  <br /> <br />
                  <Typography component="h2">Savings Rate</Typography>
                  <Typography component="p" variant="h5">
                    {data.data.savings_rate.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleOpen}
                    sx={{ marginTop: 15 }}
                  >
                    Integrate New
                  </Button>
                  <Dialog open={open} onClose={handleClose}>
                    <DialogTitle>Add New Bank Account</DialogTitle>
                    <DialogContent>
                      <TextField
                        label="Bank Name"
                        value={bankName}
                        onChange={handleBankNameChange}
                        fullWidth
                        margin="normal"
                      />
                      <TextField
                        label="Account Number"
                        value={accountNumber}
                        onChange={handleAccountNumberChange}
                        fullWidth
                        margin="normal"
                      />
                      <TextField
                        label="Mobile Number"
                        value={accountNumber}
                        onChange={handleAccountNumberChange}
                        fullWidth
                        margin="normal"
                      />
                      <TextField
                        label="Branch Location"
                        value={accountNumber}
                        onChange={handleAccountNumberChange}
                        fullWidth
                        margin="normal"
                      />
                    </DialogContent>
                    <DialogActions>
                      <Button onClick={handleClose} color="primary">
                        Cancel
                      </Button>
                      <Button onClick={handleSubmit} color="primary">
                        Add Account
                      </Button>
                    </DialogActions>
                  </Dialog>
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper
                  sx={{ p: 2, display: "flex", flexDirection: "column" }}
                ></Paper>
                <Box sx={{ width: "100%", bgcolor: "background.paper" }}>
                  <Tabs value={value} onChange={handleChange} centered>
                    <Tab label="Expenses" />
                    <Tab label="Income" />
                    <Tab label="Spending categories" />
                    <Tab label="Exceed Budget categories" />
                  </Tabs>
                  <Box
                    sx={{ display: "flex", justifyContent: "center", mt: 2 }}
                  >
                    {value === 0 && (
                      <img src={lineExpImagePath} alt="expense line chart" />
                    )}
                    {value === 1 && (
                      <img src={lineIncImagePath} alt="income line chart" />
                    )}
                  </Box>
                  {value === 2 && <TableComponent />}
                  {value === 3 && <ExceedBudgetTableComponent />}
                </Box>
              </Grid>
            </Grid>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
