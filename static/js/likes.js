function likePost(postId) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
    fetch(`/post/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likeCount = document.querySelector(`#like-count-${postId}`);
            const likeButton = document.querySelector(`#like-button-${postId}`);
            
            likeCount.textContent = data.likes;
            likeButton.classList.toggle('liked');
        }
    });
}

function followUser(userId) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
    fetch(`/auth/user/${userId}/follow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const followButton = document.querySelector('#follow-button');
            followButton.textContent = data.following ? 'Unfollow' : 'Follow';
        }
    });
}

