import { GlobalStyle } from "./pages/GlobalStyles";
import FakeNewsScreen from "./pages/fakenews";

const App:React.FC = () => {
  return(
    <>
      <GlobalStyle/>
      <FakeNewsScreen/>
    </>
  )
}

export default App;
