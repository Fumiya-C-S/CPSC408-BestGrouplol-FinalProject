import ItemCard from "./ItemCard"; 
import NavBar from "./NavBar";
import {useState, useEffect} from "react"
function App() {
  const [cartItems, setcartItems] = useState([])
  const addToCart = (product_id) => {
        const newCartList = ([...cartItems, product_id])
        console.log("Cart so far is: ", newCartList)
        setcartItems(newCartList)
    }
  const myUrl = "http://127.0.0.1:8000/products/"
  const [products, setProducts] = useState([]);
  useEffect(() => {
    const fetchProducts = async() => {
      const response = await fetch(myUrl)
      const products = await response.json()
      console.log(products)
      setProducts(products)
    }
    fetchProducts()
  }
,[])
  return(
  <>
  <NavBar></NavBar>
  {/* <div className = "page-display"> */}
  <div className = 'item-display'>
  {products.map((product) => (<ItemCard key = {product.productID} title = {product.Name} description = {product.Description} price = {product.Price} productID = {product.ProductID} category = {product.Category} onClick = {addToCart}></ItemCard>))}
  </div>
  </>);
}
export default App
