function AddButton(props) {
    return(<button onClick = {() => props.onClick({productID: props.productID, title: props.title, description: props.description, category: props.category, price: props.price})} className = 'add-button'>Add to Cart</button>);
}
export default AddButton