

// For Serach

        $(document).ready(function () {
            let debounceTimer;
            let selectedIndex = -1; // current highlighted item

            function searchBlogs(query) {
                if (!query) {
                    $('#search-results').hide();
                    selectedIndex = -1;
                    return;
                }

                $.ajax({
                    url: "{% url 'blog_search_ajax' %}", // AJAX view
                    data: { 'q': query },
                    dataType: 'json',
                    success: function (data) {
                        $('#search-results').html(data.html).show();
                        selectedIndex = -1; // reset selection
                    }
                });
            }

            $('#search-query').on('keyup', function (e) {
                const query = $(this).val();
                const items = $('#search-results li');

                // Up arrow
                if (e.keyCode === 38) {
                    if (items.length === 0) return;
                    selectedIndex = (selectedIndex <= 0) ? items.length - 1 : selectedIndex - 1;
                    items.removeClass('active');
                    $(items[selectedIndex]).addClass('active');
                    return;
                }

                // Down arrow
                if (e.keyCode === 40) {
                    if (items.length === 0) return;
                    selectedIndex = (selectedIndex >= items.length - 1) ? 0 : selectedIndex + 1;
                    items.removeClass('active');
                    $(items[selectedIndex]).addClass('active');
                    return;
                }

                // Enter key → navigate to selected item
                if (e.keyCode === 13) {
                    if (selectedIndex >= 0) {
                        const link = $(items[selectedIndex]).find('a').attr('href');
                        if (link) window.location.href = link;
                    }
                    return; // prevent default submit if navigating
                }

                // Otherwise, normal search typing
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    searchBlogs(query);
                }, 50); // debounce
            });

            // Hover on items → highlight
            $(document).on('mouseenter', '#search-results li', function () {
                $('#search-results li').removeClass('active');
                $(this).addClass('active');
                selectedIndex = $(this).index();
            });

            // Hide dropdown on outside click
            $(document).on('click', function (e) {
                if (!$(e.target).closest('.widget-search').length) {
                    $('#search-results').hide();
                    selectedIndex = -1;
                }
            });
        });
