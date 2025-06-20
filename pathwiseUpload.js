const admin = require("firebase-admin");
const fs = require("fs");
const path = require("path");

const serviceAccount = JSON.parse(
  Buffer.from(process.env.PATHWISE_SERVICE_ACCOUNT, "base64").toString("utf8")
);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

const PATHWAYS_DIR = path.join(process.cwd(), "pathways");
const ONTOLOGY_PATH = path.join(process.cwd(), "pathwise_ontology.json");

async function uploadPathways() {
  const collection = db.collection("pathways");
  const files = fs.readdirSync(PATHWAYS_DIR);

  for (const file of files) {
    const json = JSON.parse(fs.readFileSync(path.join(PATHWAYS_DIR, file)));
    const pathwayId = path.basename(file, ".json");
    json.aop_id = pathwayId;
    await collection.doc(pathwayId).set(json);
    console.log(`✅ Uploaded Pathway: ${pathwayId}`);
  }
}

async function uploadOntology() {
  const ontology = JSON.parse(fs.readFileSync(ONTOLOGY_PATH));
  const baseCollection = db.collection("ontology");

  for (const category of ontology.categories) {
    const categoryName = category.category.replace(/\s+/g, "_").toLowerCase();
    for (const term of category.terms) {
      const docId = term.id.replace(/[\/.#$\[\]]/g, "-");
      await baseCollection.doc(categoryName).collection("terms").doc(docId).set(term);
    }
    console.log(`✅ Uploaded ${category.terms.length} terms to /ontology/${categoryName}`);
  }
}

(async () => {
  await uploadPathways();
  await uploadOntology();
})();
