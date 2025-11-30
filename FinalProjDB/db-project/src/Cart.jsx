import cartImg from './assets/cart.png'
import {Link} from 'react-router-dom'
function Cart() {
    return (<>
    <div className = "cart-display">
        <Link to = '/cart'>
        <img className = 'cart-img' src = {cartImg} ></img>
        </Link>
    </div>
    </>);
}
export default Cart