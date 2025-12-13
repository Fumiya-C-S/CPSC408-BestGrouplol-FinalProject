function AddButton(props) {
    {/* Button to add to cart. Passed in an onClick function with other arguements using props like productId, title..etc*/}
    return(<button onClick = {() => props.onClick({productID: props.productID, title: props.title, description: props.description, category: props.category, price: props.price})} className = 'add-button'>Add to Cart</button>);
}
export default AddButton
