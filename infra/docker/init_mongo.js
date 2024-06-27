db = db.getSiblingDB('timeappdb');

db.createUser({
  user: 'timeapp',
  pwd: 'password',
  roles: [
    {
      role: 'readWrite',
      db: 'timeappdb',
    },
  ],
});



db.createCollection(process.env.MONGODB_COLLECTION_USER);
db.createCollection(process.env.MONGODB_COLLECTION_CATEGORY);
db.createCollection(process.env.MONGODB_COLLECTION_INTERVAL);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEDAY);
db.createCollection(process.env.MONGODB_COLLECTION_TIMEALL);
