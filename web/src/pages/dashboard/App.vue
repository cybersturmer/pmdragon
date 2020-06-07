<template>
  <div id="app" class="d-block">
    <nav class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow text-center">
      <a class="navbar-brand col-lg-1 mr-0 px-3" href="#">PmDragon</a>
      <button class="navbar-toggler position-absolute d-md-none collapsed" type="button"
              data-toggle="collapse" data-target="#sidebarMenu"
              aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <ul class="navbar-nav bg-secondary px-3">
        <li class="nav-item text-nowrap">
          <a class="nav-link font-weight-bold" href="#">
            Log out&nbsp;
            <LogOutIcon size="1.5x"></LogOutIcon>
          </a>
        </li>
      </ul>
    </nav>
    <div class="container-fluid bg-dark">
      <div class="row">
        <nav id="leftMenu" class="col-lg-1 d-md-block bg-dark sidebar collapse">
          <div class="sidebar-sticky">
            <ul class="nav text-center">
              <li class="nav-item w-100">
                <router-link class="nav-link text-light"
                             active-class="bg-secondary"
                             :to="{ name: 'backlog' }">
                  <div class="w-100">
                    <ClipboardIcon size="1.5x" class="text-light"></ClipboardIcon>
                  </div>
                  <div class="w-100 mt-1">
                    Backlog
                  </div>
                </router-link>
              </li>
              <li class="nav-item w-100">
                <router-link class="nav-link text-light"
                             active-class="bg-secondary"
                             :to="{ name: 'boards' }">
                  <div class="w-100">
                    <ArchiveIcon size="1.5x" class="text-light"></ArchiveIcon>
                  </div>
                  <div class="w-100 mt-1">
                    Board
                  </div>
                </router-link>
              </li>
            </ul>
          </div>
        </nav>
        <main role="main" class="col overflow-hidden">
          <router-view/>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ClipboardIcon,
  ArchiveIcon,
  LogOutIcon,
} from 'vue-feather-icons';

export default {
  name: 'Dashboard',
  components: {
    ClipboardIcon,
    ArchiveIcon,
    LogOutIcon,
  },
  watch: {
    $route(to) {
      document.title = to.meta.title || '~PMDragon~';
    },
  },
};
</script>
<style>
  .sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100; /* Behind the navbar */
    padding: 0 0 0; /* Height of navbar */
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
  }

  @media (max-width: 767.98px) {
    .sidebar {
      top: 5rem;
    }
  }

  .sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: .5rem;
    overflow-x: hidden;
    overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
  }

  @supports ((position: -webkit-sticky) or (position: sticky)) {
    .sidebar-sticky {
      position: -webkit-sticky;
      position: sticky;
    }
  }

  .sidebar .nav-link {
    font-weight: 500;
    color: #333;
  }

  .sidebar .nav-link .feather {
    margin-right: 4px;
    color: #999;
  }

  .sidebar .nav-link.active {
    color: #007bff;
  }

  .sidebar .nav-link:hover .feather,
  .sidebar .nav-link.active .feather {
    color: inherit;
  }

  .sidebar-heading {
    font-size: .75rem;
    text-transform: uppercase;
  }

  /*
   * Navbar
   */

  .navbar-brand {
    padding-top: .75rem;
    padding-bottom: .75rem;
    font-size: 1.25rem;
    background-color: rgba(0, 0, 0, .25);
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .25);
  }

  .navbar .navbar-toggler {
    top: .25rem;
    right: 1rem;
    padding: 0.1rem;
  }

  .navbar {
    padding: .75rem 1rem;
    border-width: 0;
    border-radius: 0;
  }
</style>
