---
title: 'Front-end Wars: Ember vs Mithril'
teaser: Conclusions from actual projects
---

JavaScript fatigue is [a thing](https://medium.com/@ericclemmons/javascript-fatigue-48d4011b6fc4). When you commit to any framework, your investment will pay itself back... but how soon and how much? If you stick to your first choice, can you really judge it accurately? Try many, and your time and mental resources get spread thin. To solve this dilemma, I limited my scope during 2016 on things that for some ethereal reason gelled with me. I've worked with Ember (v2.10) and Mithril (v1.0) on personal projects and React+Redux on a commercial project. In this retrospective I'll focus on the former two.

### Scope

Mithril and Ember are both comprehensive. In order to compare apples with apples, I'm going to compare the following related concepts which they both address:

- Views
- Components
- Data binding

## Views: templates and vnodes

Ember views are expressed in [Handlebars](http://handlebarsjs.com/) templates, while Mithril by default uses plain JavaScript to construct virtual DOM nodes. Compare Ember and Mithril snippets producing similar results:

```handlebars
<div class="container">
	<button {{action "doSomething"}}>{{label}}</button>
</div>
```

```javascript
m('.container', 
    m('button', { onclick: doSomething }, vnode.attrs.label))
```

Having your view expressed in code in (potentially the same file) is an important distinction. Handlebars, similar to [Mustache](https://mustache.github.io/) wants the template to be dumb. That is, to not contain any logic. To that end, the template language constructs are kept to a minimum, and any extension needs to be written [as a helper](https://guides.emberjs.com/v2.11.0/templates/writing-helpers/). As a Handlebars/Mustache user you are left wondering "Is joining an array of strings with a comma separator really **logic**?". Regardless of your answer, you have to implement outside of the template in (most likely) the view-model. Mithril on the other hand, does not impose any such guard rails. Giving you more power to do in-view transformations without context switches. This, however, puts the responsibility of keeping business logic out of our presentation layer, entirely on the developer.

### Components: UI building blocks

Like everything else in Ember, Components use the object model. In case you're new to Ember: there are a lot of concepts to learn in order to fully understand the framework. Ember applications live inside a container object that takes care of wiring together controllers, services and components. Ember also has its own class extension mechanism, and an object model which includes extensions to native arrays so that it can monitor changes to trigger redraws and calculate computed properties and other multi-directional binding magic. All these concepts come to a head in the `Ember.Component` class. Here is some sample code behind the Ember template from the previous chapter.

```javascript
let Component = Ember.Component.extend({
    // lifecycle method called after DOM render
    didRender() {
        // do some manual stuff to DOM
    },
    actions: {
        doSomething() {
            // perform some action 
        }
    }
})
```

Mithril defines a different lifecycle for components, but the concept is similar. It may be an implementation detail, but components in Mithril are an extension to its virtual DOM representation. In order to understand components in Mithril, you have to become familiar with at least part of its `vnode` structure, lifecycle and rendering capabilities. Mithril has a much more bare-bones feel to components. Developers have more choices they are allowed/forced to make (depending on your perspective).

```javascript
var Component = {
    onCreate: function(vnode) {
        // do some manual stuff to DOM, which is 
        // available through vnode.dom
    },
    view: function() {/* see previous chapter */}
}
```

This snippet doesn't contain a definition of your actions, because there is no one way to do this. You can define your action functions anywhere you like. I like putting them in the `vnode.state` object so I can reference them through `this.doSomething`, but it's entirely up to you the developer.

### Data binding

Data binding here is informally defined as: anything the frameworks provide that serves to read from and write to, the UI and external API's.

#### API

On the API side of things, there is the super sophisticated **Ember Data** module. It abstracts the access to relational data records, but you need either a compatible API backend or to write your own adapter in the frontend. After looking at my options, I decided *against* using Ember Data. So, my API access made use of plain JQuery XHR functions. Take note: this **is** idiomatic Ember. Many Ember examples use the embedded JQuery that it provides for this purpose, so there is nothing out of the ordinary going on here.

Mithril has its own Promise-based XHR wrapper that handles query-string construction and path parameter interpolation. No need to add a dependency on a fetch API polyfill or axios, unless you seriously prefer them.

#### Two-way data binding

The thing Angular was famous for. The simplest example of two way data binding: an input field bound to some model property. In Ember:

```handlebars
{{input type="text" value=firstName}}
```

In Mithril:

```javascript
m("input", 
  { oninput: m.withAttr("value", firstName), 
    value: firstName()})
```

In the Ember snippet, we use a template helper and `firstName` refers to a property in the template's [current rendering context](https://guides.emberjs.com/v2.0.0/templates/handlebars-basics/), which is a Component or Controller object. In the Mithril snippet, `firstName` is a getter+setter function which serves as a mutable value holder called a [Stream](http://mithril.js.org/stream.html).

#### Computed properties

In Ember computed properties have extensive support. That is, a synthetic property that depends on other properties. When any of the values of its upstream properties change, Ember triggers the re-generation of the computed value. Here is an example straight from the guide (note the use of ES6 template literals, which is not part of Ember):

```javascript
Person = Ember.Object.extend({
  // these will be supplied by `create`
  firstName: null,
  lastName: null,

  fullName: Ember.computed('firstName', 'lastName', function() {
    return `${this.get('firstName')} ${this.get('lastName')}`;
  })
});

let ironMan = Person.create({
  firstName: 'Tony',
  lastName:  'Stark'
});

ironMan.get('fullName'); // "Tony Stark"
```

Mithril has the Stream object. It allows for stringing together values in an update chain. The documentation likens it to spreadsheet cells.

```javascript
var a = stream("hello")
var b = stream("world")

var greeting = stream.merge([a, b]).map(function(values) {
    return values.join(" ")
})

console.log(greeting()) // logs "hello world"
```

### The measure

I have to explain the frame within which I'm evaluating my experiences. In recent years I've become increasingly aware of the burden that complex tools are. Any complexity, outside of the (admittedly arbitrary) scope of the problem you're solving is incidental. Complex tools can, and usually do make things easy (as evidenced by many popular examples), but when they break or we push them to the limits of their inteded purposes... how complex do you want them to be then? If you could choose, in your most dire moments of puzzle solving, what factors would you weigh? Judging the merits of frameworks by the number of Stackoverflow questions is... wrong, just wrong. That number is a product of popularity, size and complexity. Hammers don't have user manuals.

Mithril introduces fewer 'new' concepts than Ember. None of the concepts are truly new, but there are always exceptions and implementation details that one needs to be aware of, so you can only ignore documentation so much. To understands Ember you have to get a hang of:

- Handlebars
- Template helpers are essential
- What services are and what is referred to when the documentation uses the word 'container'
- The object model, especially to understand what triggers redraws, and what doesn't

To understand Mithril you need to understand

- What a `vnode` is and how they map to the actual DOM
- What a component vnode is and how it's different from the regular ones
- What triggers redraws and when to manually trigger redraws

There's more to both frameworks and these points may not be grouped very intuitively, but these are what I consider the bare necessities. Both frameworks have routers. Ember also has a CLI that (if you're just starting out) you would most likely have to get acquainted with. However, in their core they're both just ways to present data in HTML. In that respect, Mihtril is less about imposing a structure than Ember is. Ember is more about pushing you towards good separation of concerns. You can screw up and make spaghetti code with any framework, but Ember (with its guides and concepts) really tries hard to get you halfway there. However, no amount of hand-holding can force someone to understand your framework's intentions. Mithril touts best-practices, but they're easier to miss or ignore. Mithril treats you like a grown-up and let's you learn on your own. Ember is about sharing knowledge and distilling it into an evolving "Ember way" of doing things. Mithril is about simplicity and elegance. Ember is about thoroughness and ease.

All in all I think both frameworks have a similar learning curve, with Ember taking a bit more time to master. Ember simply does more, so there's more to learn that is part of Ember. A Mithril project still needs a build script and a method for managing state. Since you choose those yourself, that doesn't fall under the "learn Mithril" category. Mithril speaks to me more at this point in my career. I believe I'm at the point where I'm able to make good informed decisions and trade-offs when it comes to managing state and general software design. Ember has some powerful features, like nested routes and everything Ember Data does. Yet, these solve problems I don't yet have. Writing code as needed, I can master every aspect of my project as I get around to it.
