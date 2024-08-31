const mongoose = require('mongoose');
const { Schema } = mongoose;

// User Schema
const UserSchema = new Schema({
    name: String,
    email: { type: String, unique: true },
    password: String
});

const User = mongoose.models.User || mongoose.model('User', UserSchema);

// Stock Schema
const StockSchema = new Schema({
    name: String,
    quantity: Number,
    imageUrl: String,
    price: Number,
    date: Date,
    
    date_achat: Date,
    category: String, // Ajouté
    date_de_validite: Date,
    seuil:Number
});

const Stock = mongoose.models.Stock || mongoose.model('Stock', StockSchema);

// Product Schema
const ProductSchema = new Schema({
    name: String,
    imageUrl: String,
    description: String,
    price: Number,
    sold: { type: Number, default: 0 },
    date_de_validite: Date,
    quantity: Number,
    category: String,
    seuil: Number,


});

const Product = mongoose.models.Product || mongoose.model('Product', ProductSchema);

const CartSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    items: [
        {
            productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
            quantity: Number
        }
    ],
    total: Number
});

const Cart = mongoose.models.Cart || mongoose.model('Cart', CartSchema);

// Seller Schema
const SellerSchema = new Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    secteur_de_vente: String,
    company: String,
    cin: String,
    phone_number: String,
    address: String
}, { collection: 'seller' });

const Seller = mongoose.models.Seller || mongoose.model('Seller', SellerSchema);

const orderSchema = new mongoose.Schema({
    items: [{
        productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product', required: true },
        productName: { type: String, required: true },
        quantity: { type: Number, required: true },
        price: { type: Number, required: true }
    }],
    total: { type: Number, required: true },
    user: {
        id: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
        name: { type: String, required: true },
        email: { type: String, required: true }
    },
    date: { type: Date, default: Date.now }
});





const  Order = mongoose.models.Order || mongoose.model('order', orderSchema);


module.exports = { User, Seller, Stock, Product, Cart,Order };
