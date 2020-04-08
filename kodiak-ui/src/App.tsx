import React from 'react';
import './bootstrap.min.css'
import './App.css';
import Navbar from "./components/Navbar";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Jobs from "./pages/Jobs";
import Runs from "./pages/Runs";
import {NavbarLink} from "./types/navbar";

const links: NavbarLink[] = [
    {
        name: "Jobs",
        path: "/jobs",
        component: Jobs
    },
    {
        name: "Runs",
        path: "/runs",
        component: Runs
    }
]

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    <Navbar links={links}/>
                    <Switch>
                        {links.map(l => (
                            <Route path={l.path}>
                                {l.component}
                            </Route>
                        ))}
                    </Switch>
                </header>
            </div>
        </Router>
    );
}

export default App;
