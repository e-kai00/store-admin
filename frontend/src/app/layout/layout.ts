import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLinkActive, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-layout',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, MatButtonModule, MatIconModule],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
})
export class Layout {
  readonly isSidePanelOpen = signal(true);

  toggleSidePanel(): void{
    this.isSidePanelOpen.update((isOpen) => !isOpen)
  }
}
