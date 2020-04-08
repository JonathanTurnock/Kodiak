import React from 'react';
import {Link} from "react-router-dom";
import {NavbarLink} from "../types/navbar";

const Navbar: React.FC<{
    links: NavbarLink[]
}> = ({links}) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div style={{height: 48, display: "flex", alignItems: "center"}}>
                <img alt={"bear"} style={{height: 128, verticalAlign: "middle"}} src="/bear1.png"/>
            </div>
            <Link className="navbar-brand" to="/">Kodiak</Link>
            <div className="collapse navbar-collapse" id="navbarColor03">
                <ul className="navbar-nav mr-auto">
                    {links.map(l => (
                        <li className="nav-item">
                            <Link className="nav-link" to={l.path}>{l.name}</Link>
                        </li>
                    ))}
                </ul>
                <form className="form-inline my-2 my-lg-0">
                    <input className="form-control mr-sm-2" type="text"
                           placeholder="Search"/>
                    <button className="btn btn-secondary my-2 my-sm-0" type="submit">Search
                    </button>
                </form>
            </div>
        </nav>
    )
}

export default Navbar;