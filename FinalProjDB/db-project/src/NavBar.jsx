
import Cart from "./Cart";
function NavBar() {
    return(
        <div className = "navbar-display"> 
            <ul className = "nav-list">
                <li>Home</li>
                <li>Orders</li>
                <li>About</li>
                <li>Account</li>
            </ul>
            <Cart></Cart>
        </div>
    );
}
export default NavBar