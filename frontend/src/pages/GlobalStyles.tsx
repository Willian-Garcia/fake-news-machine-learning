import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    background-color: #ffffff;
    color: #1a1a1a;
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  textarea, input, button {
    font-family: inherit;
  }
`;
