import Cart from "./Cart";
import {Link} from 'react-router-dom'
function NavBar() {
    //Navigation bar component
    //Returns a div with a list of the different possible pages home, orders, about, and the cart component. 
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
