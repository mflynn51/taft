import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import AddPoint from './components/add-point';
import GeoPointList from './components/points-list';
import Login from './components/login';
import Signup from './components/signup';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Navbar';
import GeoDataService from './services/points';

function App() {
  const [user, setUser] = React.useState(null);
  const [token, setToken] = React.useState(null);
  const [error, setError] = React.useState('');

async function login(user = null) {
  GeoDataService.login(user)
    .then(response =>{
      setToken(response.data.token);
      setUser(response.username);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', user.username);
      setError('');
    })
    .catch( e =>{
      console.log('login', e);
        setError(e.toString());
    });
}

async function logout() {
  setToken('');
  setUser('');
  localStorage.setItem('token', '');
  localStorage.setItem('user', '');
}

async function signup(user = null) {
  GeoDataService.signup(user)
    .then(response =>{
      setToken(response.data.token);
      setUser(user.username);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', user.username);
    })
    .catch( e =>{
      console.log(e);
      setError(e.toString());
    })
}

  return (
    <div className="App">
      <Navbar bg='primary' variant='dark'>
        <Nav className='me-auto'>
          <Container>
            <Link class="nav-link" to={"/points"}>Points</Link>
            { user ? (
              <Link class="nav-link" onClick={logout}>
                Logout ({user}) </Link>
            ) : (
              <>
              <Link class="nav-link" to={"/login"}>Login</Link>
              <Link class="nav-link" to={"/Signup"}>Signup</Link>
              </>
            )}
          </Container>
        </Nav>
      </Navbar>
      <div className="container mt-4">
        <Switch>
          <Route exact path={["/", "/points"]} render={(props) =>
            <GeoPointList {...props} token={token} />
          }>
          </Route>
          <Route path="/points/create" render={(props) =>
            <AddPoint {...props} token={token} />
          }>
          </Route>
          <Route path="/points/:id" render={(props) =>
            <AddPoint {...props} token={token} />
          }>
          </Route>
          <Route path="/points/login" render={(props) =>
            <Login {...props} login={login} />
          }>
          </Route>
          <Route path="/points/signup" render={(props) =>
            <Signup {...props} signup={signup} />
          }>
          </Route>
        </Switch>
      </div>
      <footer className="text-center text-lg-start
        bg-light text-muted mt-4">
          <div className='text-center p-4'>
            @ Copyright - <a
              target="_blank"
              className="text-reset fw-bold text-decoration-none"
              href="https://twiter.com/greglim81"
              >
              Greg Lim Shot
            </a> - <a
              target="_blank"
              className="text-reset fw-bold text-decoration-none"
              href="https://twiter.com/danielgarax"
              >
              Dan Correa nBBQ
            </a>
          </div>
        </footer>
    </div>
  );
}

export default App;
