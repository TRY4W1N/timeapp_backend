print("ADSLDJKBASLKDJBALKSDJBALKSDJBAS");
print();
print();
print();

// var db = connect(process.env.MONGODB_URL);

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.createUser({
  user: process.env.MONGO_INITDB_ROOT_USERNAME,
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [
    {
      role: 'readWrite',
      db: process.env.MONGO_INITDB_DATABASE,
    },
  ],
});



db.createCollection(process.env.MONGODB_COLLECTION_USER);
db.createCollection(process.env.MONGODB_COLLECTION_CATEGORY);
db.createCollection(process.env.MONGODB_COLLECTION_INTERVAL);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEDAY);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEALL);

print("ADSLDJKBASLKDJBALKSDJBALKSDJBAS");
