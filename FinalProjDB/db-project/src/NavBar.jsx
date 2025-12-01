import { Link } from 'react-router-dom';
import Cart from "./Cart";

function NavBar() {
    return(
        <div className="navbar-display"> 
            <ul className="nav-list">
                <li><Link to="/">Home</Link></li>
                <li>Orders</li>
                <li><Link to="/about">About</Link></li>
                <li>Account</li>
            </ul>
            <Cart></Cart>
        </div>
    );
}

export default NavBar