import React, {useState, useEffect} from 'react'


// eslint-disable-next-line
import { Button, Alert, Breadcrumb, Nav, NavDropdown, Card } from 'react-bootstrap' // full library potentially
// import Button from 'react-bootstrap/Button'

import 'bootstrap/dist/css/bootstrap.min.css'


function App() {
	// DATA IS A VARIABLE BEING CREATED
	// SET DATA IS A FUNCTION

	// eslint-disable-next-line -- THIS KEEPS IT FROM GIVING NOT USED ERROR
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
	},[]) // apprently this makes it only run once
	
	return (
	<div>
		{/**/}
		{data.age_18_list}
		{data.message}
		{data.usernames_list}
		{data.file_ids_list}
		{data.session_username}
		{data.paths_list}
		{data.dates_list}
		{data.post_sources_lis}
		{data.likes}
		{data.dislikes}
		{data.searcher_has_liked}

		{data.searcher_has_disliked}
		{data.num_replies}
		{data.month_votes}
		{data.dailypool}
		{data.monthlypool}
		{data.yearlypool}
		{data.daily_left}
		{data.monthly_left}
		{data.yearly_left}
		{data.user_balance}
		
		{data.lengths_of_text_files}
		{data.source_list}
		{data.image_path_list}
		{data.distro_details_list}
		{/*{data.search_arguments}*/}
		{data.text_list}
		{data.page_no}
		{data.can_scroll}
		{data.search_favourites}
		{data.favourites_len}
		{data.uploader_is_subbed}

		<Button>TEST BUTTON</Button>
		<div>App</div>
	</div>
	)
}

export default App