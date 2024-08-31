const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const { Seller } = require('./config'); // Assurez-vous que le chemin est correct

const uri = 'mongodb://localhost:27017/e_commerce';
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });

const db = mongoose.connection;

db.on('error', console.error.bind(console, 'Erreur de connexion à MongoDB:'));
db.once('open', async () => {
    console.log('Connecté à la base de données MongoDB');

    try {
        const password = '1234'; // Mot de passe en clair
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(password, saltRounds); // Hash du mot de passe

        const newSeller = new Seller({
            name: 'chaima',
            email: 'chaima@gmail.com',
            password: hashedPassword,
            secteur_de_vente: 'Electronique',
            company: 'Tunis',
            cin: '1234567789',
            phone_number: '123-456-7890',
            address: '1234 Elm Street'
        });

        await newSeller.save();
        console.log('Vendeur ajouté avec succès');
    } catch (error) {
        console.error('Erreur lors de l\'ajout du vendeur:', error);
    } finally {
        mongoose.disconnect(); // Déconnecter après l'opération
    }
});
