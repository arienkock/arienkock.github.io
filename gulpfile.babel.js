// generated on 2016-01-05 using generator-gulp-webapp 1.0.4
import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
import browserSync from 'browser-sync';
import del from 'del';
import through from 'through2';
import swig from 'swig';
import path from 'path';
import site from './site.json';

const $ = gulpLoadPlugins({ rename: {'front-matter': 'frontMatter'}});
const reload = browserSync.reload;

gulp.task('styles', () => {
  return gulp.src('app/styles/*.scss')
    .pipe($.plumber())
    .pipe($.sourcemaps.init())
    .pipe($.sass.sync({
      outputStyle: 'expanded',
      precision: 10,
      includePaths: ['.']
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer({browsers: ['> 1%', 'last 2 versions', 'Firefox ESR']}))
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/styles'))
    .pipe(reload({stream: true}));
});

function lint(files, options) {
  return () => {
    return gulp.src(files)
      .pipe(reload({stream: true, once: true}))
      .pipe($.eslint(options))
      .pipe($.eslint.format())
      .pipe($.if(!browserSync.active, $.eslint.failAfterError()));
  };
}
const testLintOptions = {
  env: {
    mocha: true
  }
};

gulp.task('lint', lint('app/scripts/**/*.js'));
gulp.task('lint:test', lint('test/spec/**/*.js', testLintOptions));

const rePostName   = /(\d{4})-(\d{1,2})-(\d{1,2})-(.*)/;
gulp.task('posts', () => {
	return gulp.src('posts/*.md')
		.pipe($.frontMatter({property: 'page', remove: true}))
		.pipe($.marked())
		.pipe(filename2date())
		.pipe(collectPosts())
		.pipe(applyTemplate('app/post.html'))
		.pipe($.rename(function (path) {
            path.extname = ".html";
            var match = rePostName.exec(path.basename);
            if (match)
            {
                var year = match[1];            
                var month = match[2];
                var day = match[3];
            
                path.dirname = year + '/' + month + '/' + day;
                path.basename = match[4];
            }            
        }))
		.pipe(gulp.dest('.tmp'));
});
function applyTemplate(templateFile) {
    var tpl = swig.compileFile(path.join(__dirname, templateFile));
    
    return through.obj(function (file, enc, cb) {            
        var data = {
            site: site,
            page: file.page,
            content: file.contents.toString()
        };            
        file.contents = new Buffer(tpl(data), 'utf8');
        this.push(file);
        cb();
    });
}
function filename2date() {
    return through.obj(function (file, enc, cb) {                
        var basename = path.basename(file.path, '.md');
        var match = rePostName.exec(basename);
        if (match)
        {
            var year     = match[1];            
            var month    = match[2];
            var day      = match[3];
            var basename = match[4];
            file.page.date = new Date(year, month, day);
            file.page.url  = '/' + year + '/' + month + '/' + day + '/' + basename;
        }
        
        this.push(file);
        cb();
    });
}
function collectPosts() {
    var posts = [];       
    var tags = [];
    return through.obj(function (file, enc, cb) {
        posts.push(file.page);
        posts[posts.length - 1].content = file.contents.toString();
        
        if (file.page.tags) {
            file.page.tags.forEach(function (tag) {
                if (tags.indexOf(tag) == -1) {
                    tags.push(tag);
                }
            });
        }
        
        this.push(file);
        cb();
    },
    function (cb) {
        posts.sort(function (a, b) {
            return b.date - a.date;
        });
        site.posts = posts;
        site.tags = tags;
        cb();
    });
}
gulp.task('html', ['styles', 'posts'], () => {
  return gulp.src(['.tmp/**/*.html'])
    .pipe($.useref({searchPath: ['.tmp', 'app', '.']}))
    .pipe($.if('*.js', $.uglify()))
    .pipe($.if('*.css', $.cssnano()))
    .pipe($.if('*.html', $.htmlmin()))
    .pipe(gulp.dest('dist'));
});

gulp.task('html:index', ['posts'], () => {
  return gulp.src(['app/index.html', 'app/profile.html'])
        .pipe(through.obj(function (file, enc, cb) {            
            var data = {
                site: site,
                page: {} // empty object that can be extended as needed
            };
            var tpl = swig.compileFile(file.path);
            file.contents = new Buffer(tpl(data), 'utf8');
            this.push(file);
            cb();
        }))      
    .pipe(gulp.dest('.tmp'));
});

gulp.task('images', () => {
  return gulp.src('app/images/**/*')
    .pipe($.if($.if.isFile, $.cache($.imagemin({
      progressive: true,
      interlaced: true,
      // don't remove IDs from SVGs, they are often used
      // as hooks for embedding and styling
      svgoPlugins: [{cleanupIDs: false}]
    }))
    .on('error', function (err) {
      console.log(err);
      this.end();
    })))
    .pipe(gulp.dest('dist/images'));
});

gulp.task('fonts', () => {
  return gulp.src('app/fonts/**/*')
    .pipe(gulp.dest('.tmp/fonts'))
    .pipe(gulp.dest('dist/fonts'));
});

gulp.task('extras', () => {
  return gulp.src([
    'app/*.*',
    '!app/*.html'
  ], {
    dot: true
  }).pipe(gulp.dest('dist'));
});

gulp.task('clean', del.bind(null, ['.tmp', 'dist']));

gulp.task('serve', ['styles', 'fonts', 'html:index', 'posts'], () => {
  browserSync({
    notify: false,
    port: 9000,
    server: {
      baseDir: ['.tmp', 'app']
    }
  });

  gulp.watch([
    'app/*.html',
    'app/scripts/**/*.js',
    'app/images/**/*',
    '.tmp/fonts/**/*'
  ]).on('change', reload);

  gulp.watch('app/styles/**/*.scss', ['styles']);
  gulp.watch('app/fonts/**/*', ['fonts']);
  gulp.watch(['posts/**/*.md', 'app/**/*.html'], ['posts', 'html:index']);
});

gulp.task('serve:dist', () => {
  browserSync({
    notify: false,
    port: 9000,
    server: {
      baseDir: ['dist']
    }
  });
});

gulp.task('serve:test', () => {
  browserSync({
    notify: false,
    port: 9000,
    ui: false,
    server: {
      baseDir: 'test',
      routes: {
        '/scripts': 'app/scripts'
      }
    }
  });

  gulp.watch('test/spec/**/*.js').on('change', reload);
  gulp.watch('test/spec/**/*.js', ['lint:test']);
});


gulp.task('build', ['lint', 'html', 'images', 'fonts', 'extras'], () => {
  return gulp.src('dist/**/*').pipe($.size({title: 'build', gzip: true}));
});

gulp.task('default', ['clean'], () => {
  gulp.start('build');
});
