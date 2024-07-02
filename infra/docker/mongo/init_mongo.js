db = db.getSiblingDB("admin");
db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

db = db.getSiblingDB(process.env.MONGODB_DATABASE);
db.createUser({
    user: process.env.MONGODB_USERNAME,
    pwd: process.env.MONGODB_PASSWORD,
    roles: [{
        role: 'readWrite',
        db: process.env.MONGODB_DATABASE,
    }],
    mechanisms: ["SCRAM-SHA-1"],
});
db.createCollection(process.env.MONGODB_COLLECTION_USER);
db.createCollection(process.env.MONGODB_COLLECTION_CATEGORY);
db.createCollection(process.env.MONGODB_COLLECTION_INTERVAL);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEDAY);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEALL);
