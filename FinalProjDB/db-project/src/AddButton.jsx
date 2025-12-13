function AddButton(props) {
    return (
      <button
        onClick={() => props.onClick(props.productID)}
        className="add-button"
      >
        Add to Cart
      </button>
    );
  }
  
  export default AddButton;