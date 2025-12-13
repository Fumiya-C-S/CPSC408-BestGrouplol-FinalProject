import { useState, useEffect } from 'react';
import NavBar from './NavBar';

function CartPage({ cartItems = [], setCartItems }) {
  const CUSTOMER_ID = 1; // Hardcoded for now
  const [cartProducts, setCartProducts] = useState([]);

  useEffect(() => {
    // Fetch cart from database via API
    const fetchCart = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/cart/${CUSTOMER_ID}`);
        const data = await response.json();
        setCartProducts(data);
        console.log("Loaded cart from database:", data);
      } catch (error) {
        console.error("Error fetching cart:", error);
      }
    };
    fetchCart();
  }, []); // Only fetch once on mount

  const removeFromCart = async (productID) => {
    try {
      // Remove from database via API
      const response = await fetch('http://127.0.0.1:8000/cart/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          customer_id: CUSTOMER_ID,
          product_id: productID
        })
      });
      
      const data = await response.json();
      console.log(data.message);
      
      // Immediately update the cartProducts state to remove from UI
      setCartProducts(cartProducts.filter(product => product.ProductID !== productID));
      
      // Also update parent cartItems state
      const index = cartItems.indexOf(productID);
      if (index > -1) {
        const newCartItems = [...cartItems];
        newCartItems.splice(index, 1);
        setCartItems(newCartItems);
      }
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  const totalPrice = cartProducts.reduce((sum, product) => sum + (product.Price * product.Quantity), 0);

  return (
    <>
      <NavBar />
      <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
        <h1>Your Shopping Cart</h1>
        
        {cartProducts.length === 0 ? (
          <p>Your cart is empty</p>
        ) : (
          <>
            {cartProducts.map((product) => (
              <div key={product.ProductID} style={{
                border: '1px solid #ccc',
                padding: '20px',
                marginBottom: '10px',
                display: 'flex',
                gap: '20px',
                alignItems: 'center'
              }}>
                {/* Product Image */}
                <img 
                  src={`/Images/${product.Category}${product.ProductID}.png`}
                  alt={product.Name}
                  style={{
                    width: '150px',
                    height: '150px',
                    objectFit: 'contain',
                    border: '2px solid #f0f0f0',
                    padding: '10px'
                  }}
                />
                
                {/* Product Details */}
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>{product.Name}</h3>
                  <p style={{ margin: 0, color: '#666' }}>
                    {product.Description.substring(0, 100)}...
                  </p>
                  <p style={{ margin: '10px 0 0 0', fontWeight: 'bold' }}>
                    Quantity: {product.Quantity}
                  </p>
                </div>
                
                {/* Price and Remove Button */}
                <div style={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  gap: '10px',
                  alignItems: 'center' 
                }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                    ${(product.Price * product.Quantity).toFixed(2)}
                  </div>
                  <button 
                    onClick={() => removeFromCart(product.ProductID)}
                    style={{
                      backgroundColor: '#dc3545',
                      color: 'white',
                      border: 'none',
                      padding: '10px 20px',
                      borderRadius: '5px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: 'bold'
                    }}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#c82333'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#dc3545'}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
            
            <div style={{ 
              marginTop: '20px', 
              fontSize: '1.5rem', 
              textAlign: 'right',
              fontWeight: 'bold',
              padding: '20px',
              borderTop: '2px solid #333'
            }}>
              Total: ${totalPrice.toFixed(2)}
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default CartPage;