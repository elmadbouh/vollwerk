const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');
const cleanCSS = require('gulp-clean-css');
const browserSync = require('browser-sync').create();

// CSS task
function css() {
    return gulp.src('assets/sass/main.scss')
        .pipe(sass({ outputStyle: 'expanded' }).on('error', sass.logError))
        .pipe(gulp.dest('assets/css'))
        .pipe(cleanCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('assets/css'))
        .pipe(browserSync.stream()); // Inject CSS changes into the browser
}

// JS task
function js() {
    return gulp.src(['assets/js/main.js', 'assets/js/util.js'])
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('assets/js'))
        .pipe(browserSync.stream()); // Reload browser after JS changes
}

// Watch task
function watchFiles() {
    gulp.watch('assets/sass/**/*.scss', css);
    gulp.watch(['assets/js/main.js', 'assets/js/util.js'], js);
    gulp.watch('*.html').on('change', browserSync.reload); // Watch HTML files for changes
}

// BrowserSync Serve task
function serve() {
    browserSync.init({
        server: {
            baseDir: './'
        },
        open: false // Don't automatically open a new browser window
    });

    watchFiles(); // Start watching files
}

// Build task
const build = gulp.series(css, js);

// Development task (runs build then serve)
const dev = gulp.series(build, serve);

// Default task (runs build)
exports.default = build;
exports.css = css;
exports.js = js;
exports.watch = watchFiles;
exports.build = build;
exports.serve = serve;
exports.dev = dev;
