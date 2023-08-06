        function toggleContent() {
            $('#contacts').toggle();
            $('#randomMessages').toggle();

            const button = document.getElementById('toggleContentButton');
            if (button.textContent === 'Повідомлення') {
                button.textContent = 'До чатів';
            } else {
                button.textContent = 'Повідомлення';
            }
        }

        function toggleChats() {
            const chatsContainer = document.querySelector('.chats');
            chatsContainer.classList.toggle('open');
        }





    const floatingButton = document.getElementById('floatingButton');
    let isDragging = false;
    let startY, currentY;
    let originalY, offsetY;

    floatingButton.addEventListener('mousedown', (e) => {
        isDragging = true;
        startY = e.clientY;
        originalY = parseFloat(getComputedStyle(floatingButton).transform.split(',')[5]);
        offsetY = startY - originalY;
        floatingButton.style.transition = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        currentY = e.clientY;
        const newY = currentY - offsetY;
        floatingButton.style.transform = `translateY(${newY}px)`;
    });

    document.addEventListener('mouseup', () => {
        if (!isDragging) return;
        isDragging = false;
        floatingButton.style.transition = 'transform 0.3s ease-in-out';
    });

    floatingButton.addEventListener('touchstart', (e) => {
        isDragging = true;
        startY = e.touches[0].clientY;
        originalY = parseFloat(getComputedStyle(floatingButton).transform.split(',')[5]);
        offsetY = startY - originalY;
        floatingButton.style.transition = 'none';
    });

    document.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        currentY = e.touches[0].clientY;
        const newY = currentY - offsetY;
        floatingButton.style.transform = `translateY(${newY}px)`;
    });

    document.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        floatingButton.style.transition = 'transform 0.3s ease-in-out';
    });