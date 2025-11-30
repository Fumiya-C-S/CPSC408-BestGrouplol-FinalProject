import Header from './Header.jsx'
import AddButton from './addButton.jsx';
function ItemCard(props) {
      return(
  <div className = 'item-card'>
  <Header title = {props.title} description = {props.description} price = {props.price} productID = {props.productID} category = {props.category}> 
  </Header>
  <div className = 'add-container'>
  <AddButton onClick = {props.onClick}title = {props.title} description = {props.description} price = {props.price} productID = {props.productID} category = {props.category}>
  </AddButton>
  </div>
  </div>);
}
export default ItemCard