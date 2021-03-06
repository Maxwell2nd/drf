import React from 'react';
import ReactDOM, { render } from 'react-dom';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import { Index } from './Index';
import { Comments } from './Comments';
import { Sidebar } from './Sidebar';
import { Settings } from './Settings';
import { Profile } from './Profile';
import { Followers } from './Followers'
import { Following } from './Following'


function App() {
  return (
    <BrowserRouter>
      <main>
        <Sidebar />
        <Switch>
          <Route path='/' component={Index} exact />
          <Route path='/post/:id/comments/' component={Comments} exact />
          <Route path='/settings/' component={Settings} exact />
          <Route path='/profile/:id/' component={Profile} exact />
          <Route path='/followers/:id/' component={Followers} exact />
          <Route path='/following/:id/' component={Following} exact />

          <Route component={Error} />
        </Switch>
      </main>
    </BrowserRouter>
  )
}

export default App;

const container = document.getElementById('app');
render(<App />, container);