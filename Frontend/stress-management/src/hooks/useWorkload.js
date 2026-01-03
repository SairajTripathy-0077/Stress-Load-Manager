// import { useEffect, useState } from "react";
// import { collection, onSnapshot, addDoc, deleteDoc, doc } from "firebase/firestore";
// import { auth, db } from "../firebase";

// export function useWorkload() {
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     if (!auth.currentUser) return;

//     const ref = collection(db, "users", auth.currentUser.uid, "workload");

//     const unsub = onSnapshot(ref, snap => {
//       setData(
//         snap.docs.map(d => ({ id: d.id, ...d.data() }))
//       );
//     });

//     return () => unsub();
//   }, []);

//   const addItem = async item => {
//     const ref = collection(db, "users", auth.currentUser.uid, "workload");
//     await addDoc(ref, {
//       ...item,
//       createdAt: Date.now()
//     });
//   };

//   const deleteItem = async id => {
//     await deleteDoc(
//       doc(db, "users", auth.currentUser.uid, "workload", id)
//     );
//   };

//   return { data, addItem, deleteItem };
// }
