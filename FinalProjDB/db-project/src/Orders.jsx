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
  }
,[])
    return (
        <>
        <NavBar></NavBar>
        <h1>Orders</h1>
        <div className = 'orders-container'>
        {myOrder.map((order) => (<div key = {order.OrderID} className = "order-list-item"> 
            <p>Order Number: <b>{order.OrderID}</b>   Order Date: <b>{order.OrderDate}</b>    Status: <b>{order.Status}</b></p>
        </div>
        ))}
        </div>
        </>
    );
}
export default Orders
