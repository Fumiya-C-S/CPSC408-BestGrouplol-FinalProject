import Cart from "./Cart";
import {Link} from 'react-router-dom'
function NavBar() {
    return(
        <>
        <div className = "navbar-display"> 
            <ul className = "nav-list">
                <li key = "home"><Link to = '/'>Home  </Link></li>
                <li key = "orders"> <Link to = '/orders'>Orders</Link></li>
                <li key = "about"><Link to = '/about'> About</Link></li>
                <Cart></Cart>
            </ul>
        </div>
        </>
    );
}
export default NavBar
