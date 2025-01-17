/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html", "./**/templates/**/*.html", "./static/js/**/*.js"],
    theme: {
      extend: {
        backgroundImage: {
          'movie-bg': "url('/static/images/movie-bg.jpg')",
        },
      },
    },
    plugins: [],
  }