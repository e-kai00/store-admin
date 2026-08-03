import { Component } from '@angular/core';
import { RouterOutlet, RouterLinkActive, RouterLink } from "@angular/router";


@Component({
  selector: 'app-layout',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
})
export class Layout {}
