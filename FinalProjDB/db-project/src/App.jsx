import ItemCard from "./ItemCard"; 
import NavBar from "./NavBar";
import {useState, useEffect} from "react"

function App() {
  const [cartItems, setcartItems] = useState([])
  
  const addToCart = async (product_id) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_id: 1,  // Hardcoded for now
                product_id: product_id,
                quantity: 1
            })
        });
        
        const data = await response.json();
        console.log(data.message);
        
        // Also update local state
        const newCartList = ([...cartItems, product_id])
        console.log("Cart so far is: ", newCartList)
        setcartItems(newCartList)
    } catch (error) {
        console.error("Error adding to cart:", error);
    }
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
  }, [])
  
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