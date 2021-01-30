import './App.css';
import { Switch, Route } from "react-router-dom";
import Unauthorized from "./Unauthorized"
import AuthRedirect from './AuthRedirect';
import AuthorizedHome from './Authorized'

function App() {
  return (
    <Switch>
      <Route exact path="/" component={Unauthorized} />
      <Route exact path="/redirect" component={AuthRedirect} />
      <Route exact path="/authorized" component={AuthorizedHome} />
    </Switch>
  );
}

export default App;
