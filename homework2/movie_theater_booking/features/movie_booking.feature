Feature: Movie booking
    As a movie-goer
    I want to view movies and book seats
    So that I can reserve my spot

    Scenario: Viewing the movie list
        Given a movie "Inception" exists
        When I visit the movie list page
        Then I should see "Inception" in the response

    Scenario: A seat starts out available
        Given a seat "A1" exists
        Then the seat "A1" should not be booked

    Scenario: Booking a seat reserves it
        Given a movie "Inception" exists
        And a seat "A1" exists
        And I am logged in
        When I book seat "A1" for "Inception"
        Then seat "A1" is booked for "Inception"