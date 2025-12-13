import NavBar from "./NavBar";
import {useState, useEffect} from "react"

function Orders() {
    const getOrdersUrl = "http://127.0.0.1:8000/orders/"
    const [myOrder, setMyOrder] = useState([]);
    
    useEffect(() => {
        const fetchOrder = async() => {
            const userResponse = await fetch(getOrdersUrl)
            const myOrder = await userResponse.json()
            console.log(myOrder)
            setMyOrder(myOrder)
        }
        fetchOrder()
    }, [])
    
    return (
        <>
        <NavBar></NavBar>
        <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>Orders</h1>
            <div className='orders-container'>
                {myOrder.map((order) => (
                    <div 
                        key={order.OrderID} 
                        className="order-list-item"
                        style={{
                            border: '1px solid #ddd',
                            padding: '20px',
                            marginBottom: '15px',
                            borderRadius: '8px',
                            backgroundColor: '#f9f9f9'
                        }}
                    > 
                        <p style={{ margin: 0, fontSize: '16px' }}>
                            <span style={{ fontWeight: 'normal' }}>Order Number: </span>
                            <b>{order.OrderID}</b>
                            <span style={{ margin: '0 20px' }}>|</span>
                            <span style={{ fontWeight: 'normal' }}>Order Date: </span>
                            <b>{new Date(order.OrderDate).toLocaleDateString()}</b>
                            <span style={{ margin: '0 20px' }}>|</span>
                            <span style={{ fontWeight: 'normal' }}>Status: </span>
                            <b style={{ 
                                color: order.Status === 'Delivered' ? '#28a745' : 
                                       order.Status === 'Shipping' ? '#ffc107' : '#007bff'
                            }}>{order.Status}</b>
                        </p>
                    </div>
                ))}
            </div>
        </div>
        </>
    );
}

export default Orders