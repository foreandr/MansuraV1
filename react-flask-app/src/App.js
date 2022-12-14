import React, {useState, useEffect} from 'react'

function App() {
	// DATA IS A VARIABLE BEING CREATED
	// SET DATA IS A FUNCTION
	const [data, setData] = useState([{}])
	useEffect(() => {
		fetch("http://165.227.35.71:8096/").then(
			response => response.json() // text()
		).then(
			data => {
				setData(data)
				console.log(data)
			}
		)
	},[])
	
	return (
	<div>App</div>
	)
}

export default App