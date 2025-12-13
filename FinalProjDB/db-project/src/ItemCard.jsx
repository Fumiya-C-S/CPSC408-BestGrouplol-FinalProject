import Header from './Header.jsx'
import AddButton from './addButton.jsx';
function ItemCard(props) {
      //Item card component that takes in props as an arguement. 
      //Returns a div of an item card. 
      //It indcludes a header component and an addbutton component. 
      //Fills in the necessary information based on what is passed to the props. 
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
