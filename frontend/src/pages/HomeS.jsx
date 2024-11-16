import ChatApp from "../components/UserChat";
// import {useState, useEffect} from 'react'
// import { useAuth } from '../context/AuthContext.js'
// import {useDispatch, useSelector} from 'react-redux'
// import {getUserRecomendation} from '../actions/userAction'

function HomeS() {

//   const dispatch = useDispatch()
//   const { currentUser } = "TMP"
//   const alg_data =  useSelector(state => state.getUserDataAlgo)
//   const {loading, error, recomendation} = alg_data

//   useEffect(() => {
//       dispatch(getUserRecomendation(currentUser))
//   }, [currentUser, dispatch])

    return (
        <div>
            <ChatApp />
            {/* <div className='bg-gray-500'>
            {!loading && <Row  rowID='1' title='Cos tam cos tam' list = {recomendation}/> } */}
    </div>
    );
}

export default HomeS;
