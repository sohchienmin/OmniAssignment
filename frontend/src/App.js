import React from "react";
import {
  TextField,
  Container,
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import axios from "axios";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      inputUrl: "",
      generatedUrl: "",
      showGeneratedUrl: false,
      hasError: false,
      errors: [],
      generateButtonDisabled: false
    };
  }

  handleSubmit = async () => {
    this.setState({generatedUrl: "", showGeneratedUrl: false, hasError: false, errors: [], generateButtonDisabled: true});
    axios.post("http://localhost:8080/generate_url", {
      url: this.state.inputUrl
    }).then((response) => {
      this.setState(
        {generatedUrl: response.data.url, showGeneratedUrl: true, generateButtonDisabled: false}
      );
    }).catch((error) => {
      this.setState({hasError: true, errors: error.response.data.detail, generateButtonDisabled: false});
    });
  }

  handleInputChange = (input) => {
    this.setState({inputUrl: input.target.value});
  }

  render() {
    return (
      <ThemeProvider theme={darkTheme}>
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Paper
              variant="outlined"
              sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
            >
              <Typography component="h1" variant="h5">
                URL Shortener
              </Typography>
              <Box noValidate sx={{ mt: 1 }}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="url"
                  label="URL"
                  value={this.state.inputUrl}
                  onChange={this.handleInputChange}
                />
                <Button
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                  onClick={this.handleSubmit}
                  disabled={this.state.generateButtonDisabled}
                >
                  Generate Shortened URL
                </Button>
              {this.state.showGeneratedUrl &&
                <TextField
                  margin="normal"
                  fullWidth
                  id="generatedUrl"
                  label="Generated URL"
                  value={this.state.generatedUrl}
                />
              }
              {this.state.hasError &&
                <TableContainer component={Paper}>
                  <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell>Error Message</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {this.state.errors.map((row) => (
                        <TableRow
                          key={row.msg}
                          sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                          <TableCell component="th" scope="row">
                            {row.msg}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              }
              </Box>
            </Paper>
          </Box>
        </Container>
      </ThemeProvider>
    );
  }
}

export default App;
