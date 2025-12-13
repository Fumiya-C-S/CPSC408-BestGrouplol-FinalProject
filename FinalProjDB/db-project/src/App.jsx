import ItemCard from "./ItemCard"; 
import NavBar from "./NavBar";
import {useState, useEffect} from "react"

function App() {
  const [cartItems, setcartItems] = useState([]) /* cartItems useState variable and function*/
  
  const addToCart = async (product_id) => { /* Async function to addToCart */
    try {
        /*Tries to fetch a response from the backend using post method */
        const response = await fetch('http://127.0.0.1:8000/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            /*Body portion is only set for the customer id of 1 */
            body: JSON.stringify({
                customer_id: 1,  
                product_id: product_id,
                quantity: 1
            })
        });
        /* Awaits to get the response in a json format */
        const data = await response.json();
        console.log(data.message);
      
        // Also update local state
        const newCartList = ([...cartItems, product_id])
        console.log("Cart so far is: ", newCartList)
        setcartItems(newCartList) //Sets cart items
    } catch (error) { //Catches if an error occurs. 
        console.error("Error adding to cart:", error);
    }
  }
  
  const myUrl = "http://127.0.0.1:8000/products/" //Url for products
  const [products, setProducts] = useState([]); //Use state products variable and funcition
  
  useEffect(() => { //useEffect to fetch products
    const fetchProducts = async() => {
      const response = await fetch(myUrl) //Awaits fetch from the url
      const products = await response.json() //Awaits the to get the response in a json format
      console.log(products) 
      setProducts(products) //Sets products
    }
    fetchProducts() //Calls fetchProducts
  }, [])
  
  return(
  <>
  <NavBar></NavBar> {/* Nav Bar */}
  {/* Div for item-display*/}
  <div className = 'item-display'>
  {/* Uses maps products to showcase each product in an itemCard format*/}
  {products.map((product) => (<ItemCard key = {product.productID} title = {product.Name} description = {product.Description} price = {product.Price} productID = {product.ProductID} category = {product.Category} onClick = {addToCart}></ItemCard>))}
  </div>
  </>);
}

export default App
