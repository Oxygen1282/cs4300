Feature: Movie booking
    As a movie-goer
    I want to view movies and book seats
    So that I can reserve my spot

    Scenario: Viewing the movie list
        Given a movie "Inception" exists
        When I visit the movie list page
        Then I should see "Inception" in the response