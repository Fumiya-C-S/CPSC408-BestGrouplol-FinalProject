import keyPic from './assets/keyboard1.png'
function Header(props) {
    return (
        <>
        <div className = 'item'>
            <img className = 'img' src = {`/Images/${props.category}${props.productID}.png`} ></img>
            <p className = 'item-title'> {props.title}</p>
            <p className = 'item-description'>{props.description}</p>
            <p className = 'item-price'>{"$" + props.price}</p>
        </div>
        {/* <div className = 'add-container'>
            <AddButton/>
        </div> */}
        </>
    );
}
export default Header
