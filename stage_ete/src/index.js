const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require('bcrypt');
const { User, Seller, Stock, Product, Cart, Order } = require('./config');
const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/e_commerce', { useNewUrlParser: true, useUnifiedTopology: true });

const db = mongoose.connection;

db.on('error', console.error.bind(console, 'Connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

// Middleware
app.use(express.json());
app.use(express.static("public"));
app.use(express.urlencoded({ extended: false }));
app.set("view engine", "ejs");



// Routes
app.get("/", (req, res) => {
    res.render("pre_login");
});

app.get("/login", (req, res) => {
    res.render("login");
});

app.get("/signup", (req, res) => {
    res.render("signup");
});

app.get("/ajouter_produit", (req, res) => {
    res.render("ajouter_produit");
});

app.get("/home", async (req, res) => {
    try {
        const { userId } = req.query;

        if (!userId) {
            return res.status(400).send('User ID is required.');
        }

        const products = await Product.find(); // Fetch all products from the database
        res.render('home', { products, userId });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching products');
    }
});

app.get("/logseller", (req, res) => {
    res.render("logseller");
});

// Route to show product addition form
app.get('/ajouter-produit', (req, res) => {
    res.render('ajout_product');
});
app.get('/pre_login', (req, res) => {
    res.render('pre_login');
});
// Route for search functionality
app.get('/search', async (req, res) => {
    const query = req.query.query;
    try {
        // Ensure that the query is provided
        if (!query) {
            return res.status(400).send("Query is required.");
        }

        // Use the Product model for the search
        const products = await Product.find({
            name: { $regex: query, $options: 'i' }  // Case-insensitive search
        });

        // Render the home page with search results
        res.render('home', { products, userId: req.query.userId });
    } catch (error) {
        console.error('Error during search:', error);
        res.status(500).send("Error during search");
    }
});

// Route to handle product addition
app.post('/ajouter-produit', async (req, res) => {
    try {
        const { name, brand, desc, price, image } = req.body;

        if (!name || !brand || !desc || !price || !image) {
            return res.status(400).send('All fields are required.');
        }

        const newProduct = new Product({
            name,
            brand,
            description: desc,
            price,
            imageUrl: image
        });

        await newProduct.save();
        res.redirect('/home');
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.post("/signup", async (req, res) => {
    try {
        const { name, email, password } = req.body;

        if (!name || !email || !password) {
            return res.status(400).send('All fields are required.');
        }

        const existingUser = await User.findOne({ email });

        if (existingUser) {
            return res.status(400).send('User already exists. Please choose a different email.');
        }

        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        const newUser = new User({ name, email, password: hashedPassword });
        await newUser.save();

        res.redirect('/login');
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.post("/login", async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).send('All fields are required.');
        }

        const user = await User.findOne({ email });

        if (!user) {
            return res.status(400).send("User not found");
        }

        const isPasswordMatch = await bcrypt.compare(password, user.password);

        if (!isPasswordMatch) {
            return res.status(400).send("Incorrect password");
        }

        res.redirect(`/home?userId=${user._id}`);
    } catch (err) {
        console.error(err);
        res.status(500).send("Internal Server Error");
    }
});

app.post("/logseller", async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).send('All fields are required.');
        }

        const seller = await Seller.findOne({ email });

        if (!seller) {
            return res.status(400).send("Seller not found");
        }

        const isPasswordMatch = await bcrypt.compare(password, seller.password);

        if (!isPasswordMatch) {
            return res.status(400).send("Incorrect password");
        }

        res.redirect("/ajouter_produit");
    } catch (err) {
        console.error(err);
        res.status(500).send("Internal Server Error");
    }
});

app.post('/add-to-cart', async (req, res) => {
    try {
      const { userId, productId } = req.body;
  
      if (!userId || !productId) {
        return res.status(400).send('User ID and Product ID are required.');
      }
  
      // Trouver ou créer le panier de l'utilisateur
      let cart = await Cart.findOne({ userId });
  
      if (!cart) {
        cart = new Cart({ userId, items: [], total: 0 });
      }
  
      // Vérifier si le produit est déjà dans le panier
      const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
  
      if (itemIndex > -1) {
        // Si le produit est déjà dans le panier, augmenter la quantité
        cart.items[itemIndex].quantity += 1;
      } else {
        // Sinon, ajouter le produit au panier
        cart.items.push({ productId, quantity: 1 });
      }
  
      // Mettre à jour le total du panier
      const product = await Product.findById(productId);
      cart.total += product.price;
  
      await cart.save();
  
      res.redirect(`/home?userId=${userId}`);
    } catch (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    }
});
  
app.get('/panier', async (req, res) => {
    try {
        const { userId } = req.query;

        if (!userId) {
            return res.status(400).send('User ID is required.');
        }

        let cart = await Cart.findOne({ userId }).populate('items.productId');

        if (!cart) {
            cart = { userId, items: [], total: 0 };
        }

        // Fetch user details
        const user = await User.findById(userId);

        if (!user) {
            return res.status(404).send('User not found');
        }

        // Pass user details to the template
        res.render('panier', {
            cart,
            userName: user.name,
            userEmail: user.email
        });
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.post("/update-cart", async (req, res) => {
    try {
        const { cartId, productId, quantity } = req.body;

        if (!cartId || !productId || !quantity) {
            return res.status(400).send('All fields are required.');
        }

        let cart = await Cart.findById(cartId);

        const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);

        if (itemIndex > -1) {
            cart.items[itemIndex].quantity = quantity;
            cart.total = (await Promise.all(
                cart.items.map(async item => {
                    const product = await Product.findById(item.productId);
                    return product.price * item.quantity;
                })
            )).reduce((total, itemTotal) => total + itemTotal, 0);

            await cart.save();
        }

        res.redirect(`/panier?userId=${cart.userId}`);
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.post("/remove-from-cart", async (req, res) => {
    try {
        const { cartId, productId } = req.body;

        if (!cartId || !productId) {
            return res.status(400).send('All fields are required.');
        }

        let cart = await Cart.findById(cartId);

        const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);

        if (itemIndex > -1) {
            const item = cart.items[itemIndex];
            const product = await Product.findById(item.productId);
            cart.total -= item.quantity * product.price;
            cart.items.splice(itemIndex, 1);
            await cart.save();
        }

        res.redirect(`/panier?userId=${cart.userId}`);
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.post('/place-order', async (req, res) => {
    try {
        const { cartId, userId, userName, userEmail } = req.body;

        if (!cartId || !userId || !userName || !userEmail) {
            return res.status(400).send('Cart ID, user ID, user name, and user email are required.');
        }

        // Find the cart
        const cart = await Cart.findById(cartId).populate('items.productId');

        if (!cart) {
            return res.status(404).send('Cart not found');
        }

        // Create a new order
        const newOrder = new Order({
            items: cart.items.map(item => ({
                productId: item.productId._id,
                productName: item.productId.name, // Include the product name
                quantity: item.quantity,
                price: item.productId.price
            })),
            total: cart.total,
            user: {
                id: userId,
                name: userName,
                email: userEmail
            }
        });

        // Save the order
        await newOrder.save();

        // Update product quantities
        for (const item of cart.items) {
            const product = await Product.findById(item.productId._id);
            if (product) {
                product.quantity -= item.quantity;
                if (product.quantity <= 0) {
                    product.quantity = 0; // Set quantity to 0 if it's negative
                }
                await product.save();
            }
        }

        // Delete the cart
        await Cart.findByIdAndDelete(cartId);

        // Redirect to the order confirmation page
        res.redirect(`/order-confirmation?orderId=${newOrder._id}`);
    } catch (error) {
        console.error('Error processing order:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/order-confirmation', async (req, res) => {
    try {
        const { orderId } = req.query;

        if (!orderId) {
            return res.status(400).send('Order ID is required.');
        }

        // Fetch order with populated product details and user information
        const order = await Order.findById(orderId).populate('items.productId');
        if (!order) {
            return res.status(404).send('Order not found.');
        }

        // Render the order confirmation page with user details
        res.render('order-confirmation', { order });
    } catch (err) {
        console.error('Error fetching order:', err);
        res.status(500).send('Internal Server Error');
    }
});

const port = 5000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
