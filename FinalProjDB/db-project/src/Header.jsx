import keyPic from './assets/keyboard1.png'
function Header(props) {
    //Header component which is more like a product component. 
    // Takes in a props as a paramater and returns a div with an image, title, description, and price shown. 
    return (
        <>
        <div className = 'item'>
            <img className = 'img' src = {`/Images/${props.category}${props.productID}.png`} ></img>
            <p className = 'item-title'> {props.title}</p>
            <p className = 'item-description'>{props.description}</p>
            <p className = 'item-price'>{"$" + props.price}</p>
        </div>
        </>
    );
}
export default Header
