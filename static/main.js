$('.add-to-reading-list').click(addReadingList)

async function addReadingList() {
    const user_id = $(this).data('userid')
    const comic_id = $(this).data('comicid')
    const character_one = $(this).data('charcterone')
    const character_two = $(this).data('charctertwo')
  
    await axios.post(`/api/addreadinglist`, {
        user_id: user_id,
        comic_id: comic_id,     
        character_one: character_one,
        character_two: character_two
    })
    
    $(this).replaceWith('<a href=/reading_list>Added to Reading List</a>');
}

$('.delete-comic').click(deleteComic)

async function deleteComic() {
    const comic_id = $(this).data('comicid')
    const user_id = $(this).data('userid')

    await axios.post('/api/deletereadinglist', {
        comic_id: comic_id,
        user_id: user_id
    })
    $(this).parent().remove()
}

